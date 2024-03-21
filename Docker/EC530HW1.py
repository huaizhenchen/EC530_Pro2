import unittest
import sys
import tracemalloc
import cProfile
import logging

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def is_valid_matrix(matrix):
    logging.debug("Checking if the matrix is valid.")
    if not isinstance(matrix, list) or not all(isinstance(row, list) for row in matrix):
        logging.error("Invalid matrix: Not a list of lists.")
        return False
    return all(len(row) == len(matrix[0]) for row in matrix)

def is_numeric_matrix(matrix):
    logging.debug("Checking if the matrix is numeric.")
    if not all(all(isinstance(item, (int, float, str)) for item in row) for row in matrix):
        logging.error("Invalid matrix: Contains non-numeric elements.")
        return False
    return True

def is_within_bounds(value):
    return -sys.float_info.max <= value <= sys.float_info.max

def convert_and_check_numeric(matrix):
    logging.debug("Converting and checking if elements are within bounds.")
    for i, row in enumerate(matrix):
        for j, item in enumerate(row):
            if isinstance(item, str):
                try:
                    matrix[i][j] = float(item)
                except ValueError:
                    logging.error(f"ValueError: Cannot convert {item} to float.")
                    return False
            if not is_within_bounds(matrix[i][j]):
                logging.error(f"ValueError: {matrix[i][j]} is out of bounds.")
                return False
    return True

def matrix_multiply(A, B):
    logging.debug("Starting matrix multiplication.")
    if not (is_valid_matrix(A) and is_valid_matrix(B)):
        raise ValueError("Invalid matrices")
    if not (is_numeric_matrix(A) and is_numeric_matrix(B)):
        raise ValueError("Matrices must have numeric values")
    if not (convert_and_check_numeric(A) and convert_and_check_numeric(B)):
        raise ValueError("Values out of range")

    rows_A, cols_A = len(A), len(A[0])
    rows_B, cols_B = len(B), len(B[0])

    if cols_A != rows_B:
        raise ValueError("Incompatible matrix dimensions")
    C = [[0 for _ in range(cols_B)] for _ in range(rows_A)]
    for i in range(rows_A):
        for j in range(cols_B):
            for k in range(cols_A):
                C[i][j] += A[i][k] * B[k][j]
                if not is_within_bounds(C[i][j]):
                    logging.error("Result out of range")
                    raise ValueError("Result out of range")

    logging.debug("Matrix multiplication completed successfully.")
    return C

class TestMatrixMultiplication(unittest.TestCase):
    def test_normal_case(self):
        A = [[1, 2], [3, 4]]
        B = [[5, 6], [7, 8]]
        result = matrix_multiply(A, B)
        self.assertEqual(result, [[19, 22], [43, 50]])

    def test_incompatible_matrices(self):
        A = [[1, 2, 3], [3, 4, 5]]
        B = [[1, 2, 3], [4, 5, 6]]
        self.assertRaises(ValueError, matrix_multiply, A, B)

    def test_non_matrix_input(self):
        A = "not a matrix"
        B = [[1, 2], [3, 4]]
        self.assertRaises(ValueError, matrix_multiply, A, B)

    def test_non_numeric_elements(self):
        A = [[1, 2], [3, 'a']]
        B = [[1, 2], [3, 4]]
        self.assertRaises(ValueError, matrix_multiply, A, B)

    def test_scientific_notation_error(self):
        A = [[1, 2], [3, "1e-"]]
        B = [[1, 2], [3, 4]]
        self.assertRaises(ValueError, matrix_multiply, A, B)

    def test_result_out_of_bounds(self):
        A = [[1e308, 2], [3, 4]]
        B = [[2, 0], [1, 2]]
        self.assertRaises(ValueError, matrix_multiply, A, B)

if __name__ == '__main__':
    tracemalloc.start()

    profiler = cProfile.Profile()
    profiler.enable()

    unittest.main(exit=False)

    profiler.disable()
    profiler.print_stats(sort='time')

    snapshot = tracemalloc.take_snapshot()
    top_stats = snapshot.statistics('lineno')

    logging.info("[Top 10 memory usage]")
    for stat in top_stats[:10]:
        logging.info(stat)
