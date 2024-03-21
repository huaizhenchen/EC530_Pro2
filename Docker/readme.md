Project 1: Matrix Multiplication and Dockerization
Overview
This project includes a Python script EC530HW1.py for performing matrix multiplication with robust error handling and validation, along with a Dockerfile for containerizing the application. The Python script includes functionality for validating matrices, ensuring they contain only numeric values, and performing the multiplication operation with error checks for matrix compatibility and value bounds. The Dockerization aspect facilitates consistent execution environments and simplifies deployment processes.

EC530HW1.py
EC530HW1.py is a Python script designed to perform and test the multiplication of two matrices. It includes detailed logging and error handling to ensure the matrices are compatible for multiplication and the values within the matrices meet specified criteria. Features include:

Matrix Validation: Checks if the input is a valid matrix (list of lists) and if all rows are of equal length.
Numeric Validation: Ensures all elements within the matrix are numeric (int, float, or string representations of numbers).
Matrix Multiplication: Performs the multiplication of two matrices, including compatibility and bounds checking of the resultant values.
Unit Testing: Contains unittests to verify the functionality under various scenarios, including normal cases, incompatible matrices, non-numeric values, and out-of-bound values.
Dockerfile
The provided Dockerfile is set up to containerize the EC530HW1.py script, allowing for easy deployment and execution in isolated environments. The Dockerfile uses a Python base image and includes steps for copying the script into the container, installing necessary dependencies, and specifying the default command to run the script.
