import numpy as np


"""
Bit-Matrix
E.g.
(x1 or x2) and (!x2 or x3)
===
101000
000110
"""


def bit_matrix_valid(matrix: np.ndarray) -> bool:

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


def clauses_to_bit_matrix(clauses: set[tuple[int, ...]]) -> np.ndarray:

    num_clauses = len(clauses)

    # Count variables & create mapping to indices
    var_index_map = {}
    cur_index = 0
    for clause in clauses:
        for lit in clause:
            var = abs(lit)
            if var not in var_index_map.keys():
                var_index_map[var] = cur_index
                cur_index += 1
    num_vars = len(var_index_map.keys())

    # Initialize bit matrix
    bit_matrix = np.zeros((num_clauses, num_vars * 2), dtype=np.uint8)

    for clause_index, clause in enumerate(clauses):
        for lit in clause:
            is_negated = lit < 0
            var = abs(lit)
            bit_matrix[clause_index][2 * var_index_map[var] + (1 if is_negated else 0)] = 1

    return bit_matrix


def sort_bit_matrix(matrix: np.ndarray) -> np.ndarray:

    # Count the number of ones in each row
    ones_count = np.sum(matrix, axis=1)

    # Sort the rows based on the ones count
    sorted_indices = np.argsort(ones_count)

    # Rearrange the rows in the sorted order
    sorted_matrix = matrix[sorted_indices[::-1]]

    return sorted_matrix
