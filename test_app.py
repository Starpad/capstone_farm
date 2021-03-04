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
        self.new_animal1 = {
            'name': 'Flash' ,
            'age': '3',
            'comment': 'Flash is a good boy and likes to chase thrown things.',
            'species_id': '1'
        }
        self.new_animal2 = {
            'name': 'Hazel' ,
            'age': '2',
            'comment': 'Hazel loves carrots.',
            'species_id': '4'
        }

    def tearDown(self):
        """Executed after reach test"""
        pass
    
    def test_post_animal(self):
        res = self.client().post('/animals', json=self.new_animal1)
        data = json.loads(res.data)

        # Check for success of creation
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['animal_created'])
        
        res = self.client().post('/animals', json=self.new_animal2)
        data = json.loads(res.data)

        # Check for success of creation
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['animal_created'])

    def test_get_animals(self):
        res = self.client().get('/animals')
        data = json.loads(res.data)
        
        # Check for success of getting the json
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['animals'])

# Make the tests conveniently executable
if __name__ == "__main__":
  unittest.main()