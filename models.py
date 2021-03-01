import os
import json
from sqlalchemy import Column, String, Integer
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

DB_HOST = os.getenv('DB_HOST', '127.0.0.1:5432')
DB_USER = os.getenv('DB_USER', 'postgres')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'padpw')
DB_NAME = os.getenv('DB_NAME', 'capstone_farm')
DB_PATH = 'postgresql+psycopg2://{}:{}@{}/{}'.format(
    DB_USER, DB_PASSWORD, DB_HOST, DB_NAME
    )

# Migrate local DB into Heroku DB
# DB_PATH = ''

db = SQLAlchemy()

'''
Binds a flask application and also a SQLQlchemy service
'''

def setup_db(app, database_path=DB_PATH):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()


'''
Model Animal
'''

class Animal(db.Model):
    __tablename__ = 'animals'

    id = Column(Integer, primary_key=True)
    name = Column(String(40), unique=True, nullable = False)
    species = Column(String(100))
    age = Column(Integer, nullable = False)
    comment = Column(String(255))
    barn = db.relationship('Barn', backref='animals', lazy=True)


    def __init__(self, name, species, age, barn, comment):
        self.name = name
        self.species = species
        self.age = age
        self.comment = comment
        self.barn = barn

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
          'id': self.id,
          'name': self.name,
          'species': self.species,
          'age': self.age,
          'barn': self.barn,
          'comment': self.comment
        }


'''
Model Barn
'''

class Barn(db.Model):
    __tablename__ = 'barns'

    id = Column(Integer, primary_key=True)
    name = Column(String(40), unique=True, nullable = False)
    location = Column(String(100))
    food = Column(String(80))


    def __init__(self, name, location, food):
        self.name = name
        self.location = location
        self.food = food

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
          'id': self.id,
          'name': self.name,
          'location': self.location,
          'food': self.food
        }