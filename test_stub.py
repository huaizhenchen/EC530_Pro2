
import unittest
import os
import io
from flask import json
from app import app

class FlaskAppTestCase(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()
        if not os.path.exists(app.config['UPLOAD_FOLDER']):
            os.makedirs(app.config['UPLOAD_FOLDER'])

    def tearDown(self):
        pass

    def test_upload_file(self):
        response = self.app.post('/upload', data={
            'file': (io.BytesIO(b"dummy file content"), 'test.txt'),
        }, content_type='multipart/form-data')
        self.assertEqual(response.status_code, 200)
        self.assertIn('File test.txt uploaded successfully', response.get_data(as_text=True))

    def test_list_files(self):
        # Test file listing functionality
        response = self.app.get('/files')
        self.assertEqual(response.status_code, 200)

    def test_preview_file(self):
        filename = 'test.txt'
        response = self.app.get(f'/files/{filename}')
        self.assertEqual(response.status_code, 200)

    def test_train_model(self):
        # Test model training endpoint
        response = self.app.post('/train')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Model trained successfully', response.get_data(as_text=True))

    def test_cancel_training(self):
        # Test training cancellation
        response = self.app.post('/cancel-training')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Training cancelled', response.get_data(as_text=True))

    def test_training_progress(self):
        # Test training progress check
        response = self.app.get('/training-progress')
        self.assertEqual(response.status_code, 200)
        # Expecting some progress value, adjust as necessary
        self.assertIn('progress', json.loads(response.get_data(as_text=True)))

    def test_select_file_type(self):
        # Test selecting a valid file type
        response = self.app.post('/file-type', json={'type': 'json'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('File type json selected', response.get_data(as_text=True))

        # Test selecting an invalid file type
        response = self.app.post('/file-type', json={'type': 'invalid'})
        self.assertEqual(response.status_code, 400)
        self.assertIn('Invalid file type', response.get_data(as_text=True))

    def test_check_labels(self):
        # Test checking labels of uploaded data
        response = self.app.get('/labels')
        self.assertEqual(response.status_code, 200)
        self.assertIn('label1', json.loads(response.get_data(as_text=True))['labels'])

    def test_adjust_training_algorithm(self):
        # Test adjusting training algorithm
        response = self.app.post('/adjust-algorithm', json={'algorithm': 'new_algorithm'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('Algorithm new_algorithm adjusted', response.get_data(as_text=True))

    def test_add_training_data(self):
        # Test adding training data
        response = self.app.post('/add-data')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Training data added', response.get_data(as_text=True))

    def test_restart_training(self):
        # Test restarting training process
        response = self.app.post('/restart-training')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Training restarted', response.get_data(as_text=True))

    def test_compare_models(self):
        # Test comparing models' performances
        response = self.app.get('/compare-models')
        self.assertEqual(response.status_code, 200)
        models_performance = json.loads(response.get_data(as_text=True))['models_performance']
        self.assertTrue('model1' in models_performance and 'model2' in models_performance)

if __name__ == '__main__':
    unittest.main()
