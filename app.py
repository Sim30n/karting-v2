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
        self.race_type = race_type



@app.route('/')
def index():
    location = request.args.get("location")
    search_location = "%{}%".format(location)
    
    driver = request.args.get("driver")
    driver_name = "%{}%".format(driver)
    print(driver)

    queries = []
    if driver:
        queries.append(Driver.name.ilike(driver_name))
    if location:
        queries.append(Race.location.ilike(search_location))
    print(queries)
    

    #results = Result.query.all()
    """ Get races by location"""
    result = Result.query.join(Race).join(Driver).filter(*queries).order_by(Result.position).all()
    #result = Result.query.join(Race).join(Driver).filter(Race.location.ilike(search_location)).all()

    """ Get lap times by location and driver name """
    lap_times = Lap.query.join(Race).join(Driver).filter(*queries).all()
    print(dir(lap_times[0]))
    #print(result[0].driver.name)
    #print(dir(test_query[0]))
    #print(test_query[0].driver.name)
    #imatra = Race.query.filter_by(location="Imatra").first()
    #print(races)
    #races = ["asd", "asd2"]

    return render_template("home.html", result=result, lap_times=lap_times)

