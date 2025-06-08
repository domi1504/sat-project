import numpy as np


"""
Clauses
E.g.
(x1 or x2) and (!x2 or x3)
===
(1, 2)
(-2, 3)
"""


def are_clauses_empty(clauses: list[tuple[int, ...]]) -> bool:
    return sum(len(c) for c in clauses) == 0


def clauses_valid(clauses: list[tuple[int, ...]], variables_perfectly_1_to_n: bool = False) -> bool:

    # Check datatypes
    for clause in clauses:
        if type(clause) != tuple:
            return False
        for lit in clause:
            if type(lit) != int:
                return False

    # Variables are 1-based
    for clause in clauses:
        for lit in clause:
            if lit == 0:
                return False

    if not variables_perfectly_1_to_n:
        # Do not check following property
        return True

    # Check that only variables from exactly  [1, ..., n] (not more, not less!)
    variables = set()
    for clause in clauses:
        for lit in clause:
            variables.add(abs(lit))

    variables = sorted(list(variables))
    if variables != list(range(1, len(variables) + 1)):
        return False

    # All checks succeeded
    return True


def bit_matrix_to_clauses(bit_matrix: np.ndarray) -> list[tuple[int, ...]]:

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

