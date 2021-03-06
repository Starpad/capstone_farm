import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Animal, Species, db_drop_and_create_all

farm_guest_header = os.environ.get('GUEST')
farm_manager_header = os.environ.get('MANAGER')


class FarmTestCase(unittest.TestCase):
    # This class represents the testcases

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        '''
        self.DB_HOST = os.getenv('DB_HOST', '127.0.0.1:5432')
        self.DB_USER = os.getenv('DB_USER', 'postgres')
        self.DB_PASSWORD = os.getenv('DB_PASSWORD', 'padpw')
        self.DB_NAME = os.getenv('DB_NAME', 'capstone_farm')
        self.DB_PATH = "postgres://{}:{}@{}/{}".format(
            self.DB_USER, self.DB_PASSWORD, self.DB_HOST, self.DB_NAME)
        '''

        # Heroku DB path

        self.DB_PATH = os.environ.get('DB_PATH')

        setup_db(self.app, self.DB_PATH)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
            # db_drop_and_create_all

        # sample Animal for the tests
        self.new_animal = {
            'name': 'Flash',
            'age': '3',
            'comment': 'Flash is a good boy and likes to chase thrown things.',
            'species_id': '1'
        }

        self.new_wrong_animal = {
            'wrong': 'JSON'
        }

    def tearDown(self):
        """Executed after reach test"""
        pass

    # Test post request
    def test_post_animal(self):
        res = self.client().post('/animals', json=self.new_animal,
                                 headers={
                                     'Authorization': farm_manager_header
                                     })
        data = json.loads(res.data)

        # Check for success of creation
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['animal_created'])

    # Test post request error
    def test_post_animal_error(self):
        res = self.client().post('/animals', json=self.new_wrong_animal,
                                 headers={
                                     'Authorization': farm_manager_header
                                     })
        data = json.loads(res.data)

        # Check for success of creation
        self.assertEqual(res.status_code, 400)
        self.assertFalse(data['success'])

    # Test get request
    def test_get_animals(self):
        res = self.client().get('/animals',
                                headers={'Authorization': farm_guest_header})
        data = json.loads(res.data)

        # Check for success of the test
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['animals'])

    # Test get request for auth error
    def test_get_animals_error(self):
        res = self.client().get('/animals')
        data = json.loads(res.data)

        # Check for success of the test
        self.assertEqual(res.status_code, 500)
        self.assertFalse(data['success'])

    # Test get request for species
    def test_get_species(self):
        res = self.client().get('/species',
                                headers={'Authorization': farm_guest_header})
        data = json.loads(res.data)

        # Check for success of the test
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['species'])

    # Test get request for species error
    def test_get_species_error(self):
        res = self.client().get('/species')
        data = json.loads(res.data)

        # Check for success of the test
        self.assertEqual(res.status_code, 500)
        self.assertFalse(data['success'])

    # Test get request for animals id
    def test_get_animals_via_id(self):
        res = self.client().get('/animals/2',
                                headers={'Authorization': farm_manager_header})
        data = json.loads(res.data)

        # Check for success of the test
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['Name'])

    # Test get request for animals id error
    def test_get_animals_via_id_error(self):
        res = self.client().get('/animals/99',
                                headers={'Authorization': farm_guest_header})
        data = json.loads(res.data)

        # Check for success of the test
        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])

    # Test patch request for animals
    def test_patch_animal(self):
        json_age = {
            'age': 9
        }
        res = self.client().patch('/animals/2',
                                  json=json_age,
                                  headers={
                                      'Authorization': farm_manager_header
                                      })
        data = json.loads(res.data)

        # Check for success of the test
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['age'], json_age['age'])

    # Test patch request for animals error
    def test_patch_animal_error(self):
        json_age = {
            'iamamnoage': 9
        }
        res = self.client().patch('/animals/2',
                                  json=json_age,
                                  headers={
                                      'Authorization': farm_manager_header
                                      })
        data = json.loads(res.data)

        # Check for success of test
        self.assertEqual(res.status_code, 422)
        self.assertFalse(data['success'])

    # Test delete request for animals
    def test_delete_animal(self):
        res = self.client().delete('/animals/1',
                                   headers={
                                       'Authorization': farm_manager_header
                                       })
        data = json.loads(res.data)

        # Check for success of test
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    # Test delete request for animals error
    def test_delete_animal_error(self):
        res = self.client().delete('/animals/999',
                                   headers={
                                       'Authorization': farm_manager_header
                                       })
        data = json.loads(res.data)

        # Check for success of test
        self.assertEqual(res.status_code, 422)
        self.assertFalse(data['success'])


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
