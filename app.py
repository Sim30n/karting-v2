import os
from flask import Flask, render_template, url_for, redirect
from flask import Flask
from flask import request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
from models import *
load_dotenv()

######################################
#### SET UP OUR SQLite DATABASE #####
####################################

# This grabs our directory
#basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
# Connects our Flask App to our Database
DATABASE_URL = os.environ['DATABASE_URL']
FLASK_APP = os.environ['FLASK_APP']
FLASK_ENV = os.environ['FLASK_ENV']
DEBUG = os.environ['DEBUG']
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['FLASK_APP'] = FLASK_APP
app.config['FLASK_ENV'] = FLASK_ENV
app.config['DEBUG'] = DEBUG

db = SQLAlchemy(app)

# Add on migration capabilities in order to run terminal commands
Migrate(app,db)

class Race(db.Model):

    __tablename__ = 'races'

    id = db.Column(db.Integer,primary_key=True)
    location = db.Column(db.Text)
    race_date = db.Column(db.DateTime)
    results = db.relationship('Result',backref='race',lazy='dynamic')
    laps = db.relationship('Lap',backref='race',lazy='dynamic')

    def __init__(self,location,race_date):
        self.location = location
        self.race_date = race_date

    def __repr__(self):

        return f"{self.location}, {self.race_date}, {self.results}, {self.laps}"

    def print_results(self):
        for result in self.results:
            print(result.driver_id)

class Result(db.Model):

    __tablename__ = 'results'

    id = db.Column(db.Integer, primary_key=True)
    driver_id = db.Column(db.Integer,db.ForeignKey('drivers.id'))
    race_id = db.Column(db.Integer,db.ForeignKey('races.id'))
    position = db.Column(db.Integer)
    race_type = db.Column(db.Text)

    def __init__(self,driver_id, race_id, position, race_type):
        self.driver_id = driver_id
        self.race_id = race_id
        self.position = position
        self.race_type = race_type

class Driver(db.Model):

    __tablename__ = 'drivers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    results = db.relationship('Result',backref='driver',lazy='dynamic')
    laps = db.relationship('Lap',backref='driver',lazy='dynamic')

    def __init__(self, name):
        self.name = name

class Lap(db.Model):

    __tablename__ = 'laps'

    id = db.Column(db.Integer, primary_key=True)
    race_id = db.Column(db.Integer,db.ForeignKey('races.id'))
    driver_id = db.Column(db.Integer,db.ForeignKey('drivers.id'))
    lap_time = db.Column(db.Float)
    lap_number = db.Column(db.Integer)
    race_type = db.Column(db.Text)

    def __init__(self, race_id, driver_id, lap_time, lap_number, race_type):
        self.race_id = race_id
        self.driver_id = driver_id
        self.lap_time = lap_time
        self.lap_number = lap_number
        self.race_type = race_type

class Laptimes:
    def __init__(self, name, lap_list):
        self.name = name
        self.lap_list = lap_list

@app.route('/<location>/<race_type>')
def get_location(location, race_type):
    #location = request.args.get("location")
    search_location = "%{}%".format(location)
    
    driver = request.args.get("driver")
    driver_name = "%{}%".format(driver)

    #race_type = request.args.get("race_type")
    race_t = "%{}%".format(race_type)

    race_queries = []
    if driver:
        race_queries.append(Driver.name.ilike(driver_name))
    if location:
        race_queries.append(Race.location.ilike(search_location))
    if race_type:
        race_queries.append(Result.race_type.ilike("Race"))
        race_queries.append(Lap.race_type.ilike("Race"))

    qualifying_queries = []
    if driver:
        qualifying_queries.append(Driver.name.ilike(driver_name))
    if location:
        qualifying_queries.append(Race.location.ilike(search_location))
    if race_type:
        qualifying_queries.append(Result.race_type.ilike("Qualifying"))
        qualifying_queries.append(Lap.race_type.ilike("Qualifying"))
    
    """ Get race by location"""
    race_result = Result.query.join(Race).join(Driver).filter(*race_queries).order_by(Result.position).all()
    #result = Result.query.join(Race).join(Driver).filter(Race.location.ilike(search_location)).all()

    """ Get race lap times by location and driver name """
    race_lap_times = Lap.query.join(Race).join(Driver).filter(*race_queries).all()

    """ Get qualifying by location"""
    qualifying_result = Result.query.join(Race).join(Driver).filter(*qualifying_queries).order_by(Result.position).all()
    #result = Result.query.join(Race).join(Driver).filter(Race.location.ilike(search_location)).all()

    """ Get qualifying lap times by location and driver name """
    qualifying_lap_times = Lap.query.join(Race).join(Driver).filter(*qualifying_queries).all()

    #print(dir(result[0]))
    #print(dir(lap_times[0]))

    race_lap_matrix = make_lap_time_matrix(race_result, race_lap_times)
    qualifying_lap_matrix = make_lap_time_matrix(qualifying_result, qualifying_lap_times)
        
    return render_template("home.html", 
                           race_result=race_result, 
                           race_lap_matrix=race_lap_matrix[0],
                           race_drivers=race_lap_matrix[1],
                           race_num_of_laps=race_lap_matrix[2],
                           race_lap_class=race_lap_matrix[3],
                           qualifying_result=qualifying_result, 
                           qualifying_lap_matrix=qualifying_lap_matrix[0],
                           qualifying_drivers=qualifying_lap_matrix[1],
                           qualifying_num_of_laps=qualifying_lap_matrix[2],
                           qualifying_lap_class=qualifying_lap_matrix[3])


def make_lap_time_matrix(result, lap_times):

    # number of laps
    for lap in lap_times:
        num_of_laps = 0
        if num_of_laps < lap.lap_number:
            num_of_laps = lap.lap_number
    
    # initialize lap time matrix
    lap_matrix=[[""]*len(result) for i in range(num_of_laps+1)]
    lap_class = []

    # add drivers to lap time matrix
    for i in range(len(result)):
        lap_matrix[0][i] = result[i].driver.name
        lap_times_init =[None for i in range(num_of_laps)] 
        lap_class.append(Laptimes(result[i].driver.name, lap_times_init))

    # add lap times to lap time matrix
    for lap in lap_times:
        driver_index = lap_matrix[0].index(lap.driver.name)
        lap_num = lap.lap_number 
        lap_matrix[lap_num][driver_index] = lap.lap_time
        lap_class[driver_index].lap_list[lap_num-1] = lap.lap_time

    return lap_matrix[1:], lap_matrix[0], num_of_laps, lap_class
