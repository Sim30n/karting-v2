import os
from flask import Flask, render_template, url_for, redirect
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
load_dotenv()

######################################
#### SET UP OUR SQLite DATABASE #####
####################################

# This grabs our directory
basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
# Connects our Flask App to our Database
DATABASE_URL = os.environ['DATABASE_URL']
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Add on migration capabilities in order to run terminal commands
# Migrate(app,db)

class Race(db.Model):

    __tablename__ = 'races'

    id = db.Column(db.Integer,primary_key=True)
    location = db.Column(db.Text)
    race_date = db.Column(db.DateTime)

    def __init__(self,location,race_date):
        self.location = location
        self.race_date = race_date

    def __repr__(self):

        return f"Race {self.location} : {self.race_date}"

@app.route('/')
def index():
    #races = Race.query.all()
    #print(races)
    races = ["asd", "asd2"]
    return render_template("home.html", races=races)

