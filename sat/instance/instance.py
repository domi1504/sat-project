import numpy as np

from sat.instance.bit_matrix.bit_matrix import bit_matrix_valid, clauses_to_bit_matrix
from sat.instance.clauses.clauses import bit_matrix_to_clauses, clauses_valid


class Instance:

    def __init__(self, bit_matrix: np.ndarray):
        self.bit_matrix: np.ndarray = bit_matrix
        self.clauses: set[tuple[int, ...]] = bit_matrix_to_clauses(self.bit_matrix)
        assert bit_matrix_valid(self.bit_matrix)
        assert clauses_valid(self.clauses)

    def __str__(self):
        return f"Instance with {self.nr_vars()} variables and {self.nr_clauses()} clauses"

    def nr_clauses(self):
        return self.bit_matrix.shape[0]

    def nr_vars(self):
        return self.bit_matrix.shape[1] // 2


def get_instance_from_clauses(clauses: set[tuple[int, ...]]) -> Instance:
    matrix = clauses_to_bit_matrix(clauses)
    return Instance(matrix)

