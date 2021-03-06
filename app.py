import sys
import os
from flask import (
    Flask,
    request,
    abort,
    jsonify
    )
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import (
    setup_db,
    db_drop_and_create_all,
    Animal,
    Species
    )
import random
from auth import AuthError, requires_auth

# create option for paginating animals response

ANIMALS_PER_PAGE = 10


def paginate_animals(request, selection):

    page = request.args.get('page', 1, type=int)
    start = (page - 1) * ANIMALS_PER_PAGE
    end = start + ANIMALS_PER_PAGE

    animals = [animal.format() for animal in selection]
    active_animals = animals[start:end]

    return active_animals


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    CORS(app)
    setup_db(app)
    # cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

    '''
    uncomment the following line to initialize the datbase
    THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
    '''

    db_drop_and_create_all()

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,PATCH,POST,DELETE,OPTIONS')
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response

    # create a small start page for app

    @app.route('/')
    def start():
        animals = Animal.query.order_by(Animal.id).all()

        if animals is None:
            return jsonify({'message': 'Hello there, currently' +
                            'there is no animal here!'
                            })

        else:
            random_animal_number = random.randrange(1, len(animals) + 1)
            random_animal = Animal.query.filter(
                Animal.id == random_animal_number).one_or_none()
            random_species = Species.query.filter(
                Species.id == random_animal.species_id).one_or_none()

            return jsonify({'A message': 'Hello there,' +
                            'the animal of the day is:',
                            'Animal': random_animal.name,
                            'Comment': random_animal.comment,
                            'Species': random_species.name,
                            "Species Comment": random_species.description
                            })

    # Get request for animals

    @app.route('/animals', methods=['GET'])
    @requires_auth('get:animals')
    def get_animals(token):
        animals = Animal.query.order_by(Animal.id).all()

        # Abort if no animals are returned
        if animals is None:
            abort(404)

        # Get all animals and format them
        active_animals = {}
        for animal in animals:
            active_animals[animal.id] = animal.name

        # return the dictionary of animals and the number of animals
        return jsonify({
            'success': True,
            'animals': active_animals,
            'number': len(animals)
        })

    # get request for a specific animal id

    @app.route('/animals/<int:animal_id>', methods=['GET'])
    @requires_auth('get:animals')
    def get_animals_by_id(token, animal_id):
        animals = Animal.query.order_by(Animal.id).all()
        # Abort if no animals are returned

        if animals is None:
            abort(404)

        animal_filtered = Animal.query.filter(
            Animal.id == animal_id).one_or_none()

        if animal_filtered is None:
            abort(404)

        species = Species.query.filter(
            Species.id == animal_filtered.species_id).one_or_none()

        # return the dictionary of animals and the number of animals
        return jsonify({
            'success': True,
            'Name': animal_filtered.name,
            'Age': animal_filtered.age,
            'Species': species.name
        })

    # Get request for listing species

    @app.route('/species', methods=['GET'])
    @requires_auth('get:animals')
    def get_species(token):

        species = Species.query.order_by(Species.id).all()

        # Abort if no species are returned
        if species is None:
            abort(404)

        # Format species in a dictionary
        active_species = {}
        for specie in species:
            active_species[specie.id] = specie.name

        # return the dictionary of species and the number of species
        return jsonify({
            'success': True,
            'species': active_species,
            'number': len(species)
        })

    # post request for creating a new animal

    @app.route('/animals', methods=['POST'])
    @requires_auth('post:animals')
    def post_animal(token):

        body = request.get_json()

        new_name = body.get('name')
        new_age = body.get('age')
        new_comment = body.get('comment')
        new_species_id = body.get('species_id')

        # check if any required input is missing and abort
        if new_name is None:
            abort(400)
        if new_age is None:
            abort(400)
        if new_comment is None:
            abort(400)
        if new_species_id is None:
            abort(400)

        try:
            animal = Animal(name=new_name,
                            age=new_age,
                            comment=new_comment,
                            species_id=new_species_id)

            animal.insert()

            animals = Animal.query.order_by(Animal.id).all()
            species = Species.query.filter(
                Species.id == new_species_id).one_or_none()

            return jsonify({
                'success': True,
                'created': animal.id,
                'animal_created': animal.name,
                'species': species.name,
                'total_animals': len(animals)
            })

        except Exception as e:
            print(e)
            print(sys.exc_info())
            abort(422)

    # patch request for changing age of animal

    @app.route('/animals/<int:animal_id>', methods=['PATCH'])
    @requires_auth('post:animals')
    def patch_animals(token, animal_id):
        body = request.get_json()

        try:
            animal = Animal.query.filter(Animal.id == animal_id).one_or_none()
            if animal is None:
                abort(404)
            if 'age' not in body:
                abort(422)

            animal.age = int(body.get('age'))
            animal.update()

            return jsonify({
                'success': True,
                'animal_id': animal.id,
                'age': animal.age
            })

        except Exception as e:
            print(e)
            print(sys.exc_info())
            abort(422)

    # delete request for deleting animal

    @app.route('/animals/<int:animal_id>', methods=['DELETE'])
    @requires_auth('delete:animals')
    def delete_animals(token, animal_id):
        body = request.get_json()

        try:
            animal = Animal.query.filter(Animal.id == animal_id).one_or_none()
            if animal is None:
                abort(404)

            animal.delete()
            animals = Animal.query.order_by(Animal.id).all()

            return jsonify({
                'success': True,
                'deleted': animal.id,
                'deleted name': animal.name,
                'total_animals': len(animals)
            })

        except Exception as e:
            print(e)
            print(sys.exc_info())
            abort(422)

    # error handlers for all expected errors

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request"
        }), 400

    @app.errorhandler(404)
    def resource_not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404

    @app.errorhandler(422)
    def unprocessable_untity(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable untity"
        }), 422

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "internal server error"
        }), 500

    return app


app = create_app()


if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=8080, debug=True)
    app.run()
