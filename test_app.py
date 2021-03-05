import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Animal, Species, db_drop_and_create_all

class FarmTestCase(unittest.TestCase):
    # This class represents the testcases

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.DB_HOST = os.getenv('DB_HOST', '127.0.0.1:5432')
        self.DB_USER = os.getenv('DB_USER', 'postgres')
        self.DB_PASSWORD = os.getenv('DB_PASSWORD', 'padpw')
        self.DB_NAME = os.getenv('DB_NAME', 'capstone_farm')
        self.DB_PATH = "postgres://{}:{}@{}/{}".format(
            self.DB_USER, self.DB_PASSWORD, self.DB_HOST, self.DB_NAME)
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
            'name': 'Flash' ,
            'age': '3',
            'comment': 'Flash is a good boy and likes to chase thrown things.',
            'species_id': '1'
        }
        
        self.new_wrong_animal = {
            'wrong' : 'JSON'
        }

    def tearDown(self):
        """Executed after reach test"""
        pass
    
    def test_post_animal(self):
        res = self.client().post('/animals', json=self.new_animal)
        data = json.loads(res.data)

        # Check for success of creation
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['animal_created'])

    def test_post_animal_error(self):
        res = self.client().post('/animals', json=self.new_wrong_animal)
        data = json.loads(res.data)

        # Check for success of creation
        self.assertEqual(res.status_code, 400)
        self.assertFalse(data['success'])

    # Post test for authorization Admin

    def test_get_animals(self):
        res = self.client().get('/animals')
        data = json.loads(res.data)
        
        # Check for success of the test
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['animals'])


    def test_get_animals_via_id(self):
        res = self.client().get('/animals/1')
        data = json.loads(res.data)
        
        # Check for success of the test
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['Name'])

    def test_get_animals_via_id_error(self):
        res = self.client().get('/animals/99')
        data = json.loads(res.data)
        
        # Check for success of the test
        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])

    def test_patch_animal(self):
        json_age = {
            'age' : 9
        }
        res = self.client().patch('/animals/1', json = json_age)
        data = json.loads(res.data)
        
        # Check for success of the test
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['age'],json_age['age'])
        
    def test_patch_animal_error(self):
        json_age = {
            'iamamnoage' : 9
        }
        res = self.client().patch('/animals/1', json = json_age)
        data = json.loads(res.data)
        
        # Check for success of test
        self.assertEqual(res.status_code, 422)
        self.assertFalse(data['success'])
        
    def test_delete_animal(self):
        res = self.client().delete('/animals/1')
        data = json.loads(res.data)
        
        # Check for success of test
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_delete_animal_error(self):
        res = self.client().delete('/animals/999')
        data = json.loads(res.data)
        
        # Check for success of test
        self.assertEqual(res.status_code, 422)
        self.assertFalse(data['success'])

     # Delete test for authorization Admin


# Make the tests conveniently executable
if __name__ == "__main__":
  unittest.main()