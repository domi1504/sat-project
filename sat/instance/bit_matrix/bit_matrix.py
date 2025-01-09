import numpy as np


def bit_matrix_valid(matrix: np.array):

    # Check datatype
    if matrix.dtype != np.uint8:
        return False

    # Check if 2-dim
    if matrix.ndim != 2:
        return False

    # Check for only 0 and 1
    if list(np.unique(matrix)) != [0, 1]:
        return False

    # Check that even number of columns (2 per variable)
    if matrix.shape[1] % 2 != 0:
        return False

    return True


def sort_bit_matrix(matrix: np.ndarray):

    # Count the number of ones in each row
    ones_count = np.sum(matrix, axis=1)

    # Sort the rows based on the ones count
    sorted_indices = np.argsort(ones_count)

    # Rearrange the rows in the sorted order
    sorted_matrix = matrix[sorted_indices[::-1]]

    return sorted_matrix
