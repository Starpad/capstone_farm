import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Animal, Species, db_drop_and_create_all

farm_guest_header = 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkRrM21iVlFWUEloZUpRdEFLOTVkRCJ9.eyJpc3MiOiJodHRwczovL3N0YXJwYWQuZXUuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDYwMTgyMDhjNTIzOGZiMDA2OTYzNTRhOCIsImF1ZCI6Imh0dHBzOi8vY2FwZmFybS5oZXJva3VhcHAuY29tIiwiaWF0IjoxNjE1MDI4MzY3LCJleHAiOjE2MTUwMzU1NjcsImF6cCI6Im1LdGlvWm8zSmhnUFB5ZXVielc0bW03cUk3VmRLQWwxIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJnZXQ6YW5pbWFscyJdfQ.MLk0qX-1-OguyM9-0fCHeA8BgyRq1vRyFuKKp68-R2tR8Ww7jX8GSGA5USdNoQBdSUIdgtpcKqPVJGWRpE4DvnKQwWdM8b5G1DYAFOBZYEsBK_em73yLMgtSyBqup1lBso5hWWo5PjCpaYZG9ZCRe7AJ850mdi-sAvrGHoOZinPO54DqzTwBAFkjhlK38mCStOUxvGkgws3vfE7oovYpCO4Rg_avrZug9cKYLyapPHvYQj3wLSSmpq0q7rXDnC9r6tMENhKQp9Ori59uLYFO6nFDwA-AfC77iQkYipTM4WfRMH5LIjMmHRY2EIytXvb8GZS2JjO1qnOUEnQ5tFMI0A'
farm_manager_header = 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkRrM21iVlFWUEloZUpRdEFLOTVkRCJ9.eyJpc3MiOiJodHRwczovL3N0YXJwYWQuZXUuYXV0aDAuY29tLyIsInN1YiI6Imdvb2dsZS1vYXV0aDJ8MTA4NTA2NTgyMjIwODkxNDQzMTE3IiwiYXVkIjoiaHR0cHM6Ly9jYXBmYXJtLmhlcm9rdWFwcC5jb20iLCJpYXQiOjE2MTUwMjg2NDMsImV4cCI6MTYxNTAzNTg0MywiYXpwIjoibUt0aW9abzNKaGdQUHlldWJ6VzRtbTdxSTdWZEtBbDEiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphbmltYWxzIiwiZ2V0OmFuaW1hbHMiLCJwb3N0OmFuaW1hbHMiXX0.dvweAX76YldgjMdc0LgJzB6RUz1YgouQaiu7sb9z8OnViuwlktKIdtVT1FBTrdKBrPzvJrKCfY51N9upYPsdC5COhdn6qHIpRAk2wt4FRPwclWZlkMR0bv48caa8qGAc8o3DsFlB8csXDisdkaHSMiOJz4_l43zh1iSGtKlbAm9koAbp1shKidyRhdz5i5aoSkh0LJXJUPyWp5rckVIJsqlLkVj6PbLwQ-taQ3wJc3gPeTonLeyCe05941DUiQEMFDWW_H_2TOwib1zye57qQ4Ta3wk0bafGpuSS4RnTCKRjCOVsqhlEoEJKp879XBKHTV50WqociBIUl2m7RcAMGw'

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
        
        self.DB_PATH = 'postgres://rtmfcdettevdpc:1ab7e5292d255864ac4a0c67193aea7f994a0a5f8c16de26086b49c04206b0a4@ec2-50-19-176-236.compute-1.amazonaws.com:5432/df935uv7s2p4i8'
        
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
        res = self.client().post('/animals', json=self.new_animal, headers = {'Authorization' : farm_manager_header })
        data = json.loads(res.data)

        # Check for success of creation
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['animal_created'])

    def test_post_animal_error(self):
        res = self.client().post('/animals', json=self.new_wrong_animal, headers = {'Authorization' : farm_manager_header })
        data = json.loads(res.data)

        # Check for success of creation
        self.assertEqual(res.status_code, 400)
        self.assertFalse(data['success'])

    # Post test for authorization Admin

    def test_get_animals(self):
        res = self.client().get('/animals', headers = {'Authorization' : farm_guest_header })
        data = json.loads(res.data)
        
        # Check for success of the test
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['animals'])

    def test_get_animals_error(self):
        res = self.client().get('/animals')
        data = json.loads(res.data)
        
        # Check for success of the test
        self.assertEqual(res.status_code, 500)
        self.assertFalse(data['success'])
    
    def test_get_species(self):
        res = self.client().get('/species', headers = {'Authorization' : farm_guest_header })
        data = json.loads(res.data)
        
        # Check for success of the test
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['species'])

    def test_get_species_error(self):
        res = self.client().get('/species')
        data = json.loads(res.data)
        
        # Check for success of the test
        self.assertEqual(res.status_code, 500)
        self.assertFalse(data['success'])

    def test_get_animals_via_id(self):
        res = self.client().get('/animals/1', headers = {'Authorization' : farm_manager_header })
        data = json.loads(res.data)
        
        # Check for success of the test
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['Name'])

    def test_get_animals_via_id_error(self):
        res = self.client().get('/animals/99', headers = {'Authorization' : farm_guest_header })
        data = json.loads(res.data)
        
        # Check for success of the test
        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])

    def test_patch_animal(self):
        json_age = {
            'age' : 9
        }
        res = self.client().patch('/animals/1', json = json_age, headers = {'Authorization' : farm_manager_header })
        data = json.loads(res.data)
        
        # Check for success of the test
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['age'],json_age['age'])
        
    def test_patch_animal_error(self):
        json_age = {
            'iamamnoage' : 9
        }
        res = self.client().patch('/animals/1', json = json_age, headers = {'Authorization' : farm_manager_header })
        data = json.loads(res.data)
        
        # Check for success of test
        self.assertEqual(res.status_code, 422)
        self.assertFalse(data['success'])
        
    def test_delete_animal(self):
        res = self.client().delete('/animals/1', headers = {'Authorization' : farm_manager_header })
        data = json.loads(res.data)
        
        # Check for success of test
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_delete_animal_error(self):
        res = self.client().delete('/animals/999', headers = {'Authorization' : farm_manager_header })
        data = json.loads(res.data)
        
        # Check for success of test
        self.assertEqual(res.status_code, 422)
        self.assertFalse(data['success'])

    def test_delete_animal_error_auth(self):
        res = self.client().delete('/animals/2', headers = {'Authorization' : farm_guest_header })
        data = json.loads(res.data)
        
        # Check for success of test
        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])


# Make the tests conveniently executable
if __name__ == "__main__":
  unittest.main()