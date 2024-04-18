import unittest
from app import app, db, Dataset
from datetime import datetime
from flask_testing import TestCase

class BaseTestCase(TestCase):

    def create_app(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['TESTING'] = True
        return app

    def setUp(self):
        db.create_all()
        sample_dataset = Dataset(Name='Sample', Description='Sample dataset', Type='Sample Type', CreationDate=datetime.utcnow())
        db.session.add(sample_dataset)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

class TestDatasetAPI(BaseTestCase):

    def test_get_dataset(self):
        response = self.client.get('/datasets/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['Name'], 'Sample')

    def test_post_dataset(self):
        response = self.client.post('/datasets/', json={
            'Name': 'New Dataset',
            'Description': 'New dataset description',
            'Type': 'New Type',
            'CreationDate': '2022-01-01'
        })
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['Name'], 'New Dataset')

    def test_put_dataset(self):
        response = self.client.put('/datasets/1', json={
            'Name': 'Updated Name',
            'Type': 'Updated Type'
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['message'], 'Dataset updated successfully')

        # Fetch the updated dataset and confirm changes
        dataset = Dataset.query.get(1)
        self.assertEqual(dataset.Name, 'Updated Name')
        self.assertEqual(dataset.Type, 'Updated Type')

    def test_delete_dataset(self):
        response = self.client.delete('/datasets/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['message'], 'Dataset deleted')

        # Try to fetch the deleted dataset
        response = self.client.get('/datasets/1')
        self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    unittest.main()
