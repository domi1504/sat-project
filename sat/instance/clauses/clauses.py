import numpy as np


def create_clauses(bit_matrix: np.ndarray):
    clauses = set()
    for row in bit_matrix:
        clause = []
        for pos in np.where(row)[0]:

            # To start from 1, not from 0
            pos += 2

            if pos % 2 == 0:
                # Positive literal
                clause.append(str(pos // 2))
            else:
                # Negative literal
                clause.append("-" + str(pos // 2))

        clauses.add(tuple(clause))

    return clauses
