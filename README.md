# Machine Learning image classification API

## Introduction
The main work done in this project is through the API, so that users can locally transfer images to the server, the images will be classified on the server through the ML model for the images, and the data will be automatically saved in the database, the user can through the API for the database to CRUD operation.

## Getting Started

### Prerequisites
Ensure you have Python and Unity installed on your system. You may need additional dependencies as described in `requirements.txt`.

### Installation

1. **Server Setup:**
   - Navigate to the `pro2final` directory.
   - Install required Python packages:
     ```bash
     pip install -r requirements.txt
     ```
   - Run the server application:
     ```bash
     python app.py
     ```

2. **Unit Testing:**
   - To run unit tests for the server, execute:
     ```bash
     python test_app.py
     ```

3. **Framework Usage:**
   - Open the `framework` directory.
   - Execute the `helloworld.exe` application, designed with Unity.
   - Use the interface to upload a `.png` image, which will be sent to the server via an API. The server will process and store the recognized information in the database.

4. **Client Operations:**
   - Run the `client.py` file to manage data in the database through CRUD operations:
     ```bash
     python client.py
     ```

## Usage
After setting up the server, testing it, interacting with the Unity framework, and executing client operations, you can fully utilize the functionalities provided by this project for image processing and data management.

## Support
For additional help or issues, refer to the project documentation or submit an issue in the project repository.


## Authors
- Huaizhen Chen


