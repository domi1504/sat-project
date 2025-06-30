import numpy as np


"""
Bit-Matrix Representation for SAT Instances

This module provides utilities for converting SAT problem instances (as clauses)
into a binary matrix representation and vice versa.

Example:
    The formula (x1 ∨ x2) ∧ (¬x2 ∨ x3) can be represented as:

    Bit Matrix:
        101000
        000110

Each variable is represented using two columns:
- Column 2i represents literal xi
- Column 2i+1 represents ¬xi
"""


def bit_matrix_valid(matrix: np.ndarray) -> bool:
    """
    Validates whether a given matrix is a proper bit matrix for SAT representation.

    Checks performed:
    - Matrix is 2D
    - Data type is `np.uint8`
    - Contains only binary values (0 or 1)
    - Has an even number of columns (two per variable)

    :param matrix: Numpy array to validate.
    :return: True if the matrix is a valid bit matrix; False otherwise.
    """

    # Check datatype
    if matrix.dtype != np.uint8:
        return False

    # Check if 2-dim
    if matrix.ndim != 2:
        return False

    # Check for only 0 and 1
    values = list(np.unique(matrix))
    if any(v not in (0, 1) for v in values):
        return False

    # Check that even number of columns (2 per variable)
    if matrix.shape[1] % 2 != 0:
        return False

    return True


def clauses_to_bit_matrix(clauses: list[tuple[int, ...]]) -> np.ndarray:
    """
    Converts a list of clauses into a bit matrix representation.

    Each variable is mapped to two columns in the matrix:
    - Even index (2i) for positive literal xi
    - Odd index (2i+1) for negative literal ¬xi

    Example:
        Clause (x1 ∨ ¬x2) becomes row [1, 0, 0, 1, 0, 0] in a 3-variable instance.

    :param clauses: List of clauses, where each clause is a tuple of integers.
    :return: Bit matrix (2D numpy array) representing the clauses.
    """

    num_clauses = len(clauses)

    # Count variables & create mapping to indices
    var_index_map: dict[int, int] = {}
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
            bit_matrix[clause_index][
                2 * var_index_map[var] + (1 if is_negated else 0)
            ] = 1

    return bit_matrix


def bit_matrix_to_clauses(bit_matrix: np.ndarray) -> list[tuple[int, ...]]:
    """
    Converts a bit matrix back into a list of clauses.

    Each row of the matrix represents a clause.
    The columns are interpreted as follows:
    - For each variable xi, column 2i represents the positive literal xi
    - Column 2i+1 represents the negative literal ¬xi

    For each 1 in the matrix, the corresponding literal is added to the clause.

    Example:
        Bit matrix row: [1, 0, 0, 1] => Clause: (x1, ¬x2)

    :param bit_matrix: A binary matrix where rows correspond to clauses and
                       columns represent positive/negative literals.
    :return: List of clauses, where each clause is a tuple of integers.
    """

    clauses = []
    for row in bit_matrix:
        clause = []
        for pos in np.where(row)[0]:

            # To start from 1, not from 0
            pos += 2
            variable = int(pos // 2)

            if pos % 2 == 0:
                # Positive literal
                clause.append(variable)
            else:
                # Negative literal
                clause.append(-variable)

        clauses.append(tuple(clause))

    return clauses


def sort_bit_matrix(matrix: np.ndarray) -> np.ndarray:
    """
    Sorts the rows of the bit matrix by the number of set bits (1s) in descending order.

    This helps in organizing clauses by their literal count, potentially aiding in
    heuristics or preprocessing.

    :param matrix: Bit matrix to sort.
    :return: Sorted bit matrix with rows arranged by descending 1-count.
    """

    # Count the number of ones in each row
    ones_count = np.sum(matrix, axis=1)

    # Sort the rows based on the ones count
    sorted_indices = np.argsort(ones_count)

    # Rearrange the rows in the sorted order
    sorted_matrix = matrix[sorted_indices[::-1]]

    return sorted_matrix
