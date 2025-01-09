import numpy as np

from sat.instance.bit_matrix.bit_matrix import bit_matrix_valid
from sat.instance.clauses.clauses import create_clauses


class Instance:

    """
    Bit-Matrix
    E.g.
    (x1 or x2) and (!x2 or x3)
    ===
    101000
    000110
    """

    def __init__(self, bit_matrix: np.array):
        self.bit_matrix: np.ndarray = bit_matrix
        assert bit_matrix_valid(self.bit_matrix)
        self.clauses: set = create_clauses(self.bit_matrix)

    def __str__(self):
        return str(self.bit_matrix)

    def nr_clauses(self):
        return self.bit_matrix.shape[0]

    def nr_vars(self):
        return self.bit_matrix.shape[1] // 2

