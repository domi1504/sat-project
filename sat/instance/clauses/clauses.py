import numpy as np


def create_clauses(bit_matrix: np.ndarray):
    clauses = set()
    for row in bit_matrix:
        clause = set()
        for pos in np.where(row)[0]:
            if pos % 2 == 0:
                # Positive literal
                clause.add(str(pos // 2))
            else:
                # Negative literal
                clause.add("-" + str(pos // 2))
        clauses.add(clause)
    return clauses
