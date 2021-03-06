import os
import json
from flask import Flask
from sqlalchemy import Column, String, Integer, ForeignKey, create_engine
from sqlalchemy.orm import relationship
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

'''
DB_HOST = os.getenv('DB_HOST', '127.0.0.1:5432')
DB_USER = os.getenv('DB_USER', 'postgres')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'padpw')
DB_NAME = os.getenv('DB_NAME', 'capstone_farm')
DB_PATH = 'postgresql+psycopg2://{}:{}@{}/{}'.format(
    DB_USER, DB_PASSWORD, DB_HOST, DB_NAME
    )
'''

# Migrate local DB into Heroku DB
DB_PATH = os.environ.get('variable_name')

db = SQLAlchemy()


'''
Binds a flask application and also a SQLAlchemy service
'''


def setup_db(app, database_path=DB_PATH):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()


'''
db_drop_and_create_all()
    drops the database tables and starts fresh
    can be used to initialize a clean database
'''


def db_drop_and_create_all():
    db.drop_all()
    db.create_all()
    db_create_species()
    db_create_animals()


'''
Model Species
'''


class Species(db.Model):
    __tablename__ = 'species'

    id = Column(Integer, primary_key=True)
    name = Column(String(40), unique=True, nullable=False)
    description = Column(String(800))
    animals = db.relationship('Animal', backref="species", lazy=True)

    def __init__(self, name, description):
        self.name = name
        self.description = description

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
          'description': self.description
        }


'''
Model Animal
'''


class Animal(db.Model):
    __tablename__ = 'animals'

    id = Column(Integer, primary_key=True)
    name = Column(String(40), unique=True, nullable=False)
    age = Column(Integer, nullable=False)
    comment = Column(String(255))
    species_id = Column(Integer, ForeignKey('species.id'), nullable=True)

    def __init__(self, name, age, comment, species_id):
        self.name = name
        self.age = age
        self.comment = comment
        self.species_id = species_id

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
          'comment': self.comment,
          'species_id': self.species_id
        }


'''
Setting up a few species for Testing
'''


def db_create_species():

    species_dog = (Species(
        name='Dog',
        description='A dog is a mammal in the order Carnivora. ' +
        'The history of dogs is an old tale indeed. You could say as long as' +
        'there has been civilisation, ' +
        'there have been records of humans and dogs. Dogs were domesticated' +
        'from wolves around 15,000 years ago. ' +
        'New evidence suggests that dogs were first domesticated in East Asia,' +
        'possibly China. ' +
        'Over time, the dog has developed into hundreds of breeds with a great' +
        'degree of variation. ' +
        'Dogs, like humans, are highly social animals and this similarity' +
        'in their overall behavioural ' +
        'pattern accounts for their trainability, playfulnes and ability' +
        'to fit into human households ' +
        'and social situations. This similarity has earned dogs a unique position ' +
        'in the realm of interspecies relationships.'
    ))
    species_dog.insert()

    species_cat = (Species(
        name='Cat',
        description='Cats belong to the family called "Felidea".' +
        'Interestingly enough,' +
        'the cat family split from the other mammals at least' +
        '40,000,000 years ago, making ' +
        'them one of the oldest mammalian families. All cats' +
        'share certain characteristics ' +
        'that are unique to the cat family. Adult cats average' +
        'about 8 to 10 inches ' +
        '(20 to 25 centimetres) tall at the shoulder. Most cats' +
        'weigh from 6 to 15 pounds ' +
        '(2.7 to 7 kilograms). Some cats weigh more than 20 pounds' +
        '(9 kilograms).'
    ))
    species_cat.insert()

    species_panda = (Species(
        name='Panda',
        description='The Giant Panda (black-and-white cat-foot) ' +
        '(Ailuropoda melanoleuca) ' +
        ', is a mammal classified in the bear family, Ursidae, native' +
        'to central-western and ' +
        'southwestern China. Giant Pandas are one of the rarest mammals' +
        'in the world. Pandas ' +
        'are easily recognized by their large, distinctive black patches' +
        'around the eyes, ' +
        'over the ears and across their round body.Giant pandas live in' +
        'a few mountain ranges ' +
        'in central China, in Sichuan, Shaanxi and Gansu provinces. ' +
        'Pandas once lived in lowland ' +
        'areas, however, farming, forest clearing and other development now ' +
        'restrict giant pandas to the mountains.'
    ))
    species_panda.insert()

    species_guineapig = (Species(
        name='Guinea Pig',
        description='Guinea Pigs are hystricomorph rodents ' +
        '(related to chinchillas and porcupines) ' +
        'that originated from the Andes Mountains region of South America.' +
        'Their scientific name is ' +
        '‘Cavia Porcellus’ and so they are called ‘Cavies’ for short. ' +
        'Guinea Pigs are not Pigs at all, despite their name. Guinea Pigs' +
        'are part of the ' +
        'Rodent family which also includes rats, mice, hamsters,' +
        'squirrels and beavers. ' +
        'Guinea Pigs originated from South America where they still' +
        'live in the wild today' +
        '. In the wild Guinea Pigs tend to make their' +
        'habitats in rocky areas, ' +
        'grasslands and forests.'
    ))
    species_guineapig.insert()


def db_create_animals():

    animal1 = (Animal(
        name='Freddy',
        age='5',
        comment='Freddy is a friendly cat',
        species_id='2'
    ))
    animal1.insert()

    animal2 = (Animal(
        name='Shao',
        age='9',
        comment='Shao likes to eat all day',
        species_id='3'
    ))
    animal2.insert()
