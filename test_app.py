import os
from datetime import datetime
from config import app, db
from models import Dataset, DatasetListResource
import unittest

class TestCase(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        self.app = app.test_client()
        with app.app_context():
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_dataset_creation(self):
        response = self.app.post('/datasets', json={
            'Name': 'Test Dataset',
            'Description': 'A test dataset description',
            'Type': 'Test Type',
            'CreationDate': datetime.now().strftime('%Y-%m-%d')
        })
        self.assertEqual(response.status_code, 201)

    def test_dataset_list(self):
        response = self.app.get('/datasets')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, list)

    def test_dataset_update(self):
        # Create a dataset first
        response = self.app.post('/datasets', json={
            'Name': 'Update Test',
            'Description': 'Before update',
            'Type': 'Initial Type',
            'CreationDate': datetime.now().strftime('%Y-%m-%d')
        })
        dataset_id = response.json['DatasetID']

        # Update the dataset
        update_response = self.app.put(f'/datasets/{dataset_id}', json={
            'Name': 'Updated Name',
            'Description': 'After update',
            'Type': 'Updated Type',
            'CreationDate': datetime.now().strftime('%Y-%m-%d')
        })
        self.assertEqual(update_response.status_code, 200)
        self.assertIn('Dataset updated.', update_response.json['message'])

    def test_dataset_deletion(self):
        # Create a dataset first
        response = self.app.post('/datasets', json={
            'Name': 'Deletion Test',
            'Description': 'To be deleted',
            'Type': 'Deletable',
            'CreationDate': datetime.now().strftime('%Y-%m-%d')
        })
        dataset_id = response.json['DatasetID']

        # Delete the dataset
        delete_response = self.app.delete(f'/datasets/{dataset_id}')
        self.assertEqual(delete_response.status_code, 200)
        self.assertIn('Dataset deleted.', delete_response.json['message'])

if __name__ == '__main__':
    unittest.main()
