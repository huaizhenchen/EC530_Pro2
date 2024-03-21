## Overview
This repository contains a simple Flask application (`modelML.py`) designed for asynchronous model training and prediction with TensorFlow for MNIST-like image data. Additionally, a suite of tests (`test_modelML.py`) is provided to ensure the application's endpoints function as expected.

## modelML.py
The core application file, `modelML.py`, defines a Flask app with two main endpoints: `/train` for initiating the asynchronous training of a neural network model, and `/predict` for making predictions using the trained model with uploaded images.

### Features
- Asynchronous task management with Celery for model training.
- REST API endpoints for training initiation and image prediction.
- Integration with TensorFlow to create and utilize a neural network model.

## test_modelML.py
The `test_modelML.py` file contains tests written with pytest to validate the functionality of the Flask application. These tests ensure the application behaves correctly under various conditions, including handling requests without required data and processing image files for prediction.

### Tests Included
- Verifying the `/train` endpoint initiates model training.
- Checking the `/predict` endpoint's behavior when no image is uploaded.
- Testing the `/predict` endpoint with a valid image file.
