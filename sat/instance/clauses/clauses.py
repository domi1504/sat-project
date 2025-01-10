import numpy as np
import re


"""
Clauses
E.g.
(x1 or x2) and (!x2 or x3)
===
(1, 2)
(-2, 3)
"""


def clauses_valid(clauses: set) -> bool:

    # Check datatypes
    for clause in clauses:
        if type(clause) != tuple:
            return False
        for lit in clause:
            if type(lit) != str:
                return False

    # Check for correct literals (only form <INT> or -<INT>)
    pattern = r"^-?[1-9]\d*$"
    def matches_format(s):
        return bool(re.fullmatch(pattern, s))

    for clause in clauses:
        for lit in clause:
            if not matches_format(lit):
                return False

    # Check that only variables from exactly  [1, ..., n] (not more, not less!)
    variables = set()
    for clause in clauses:
        for lit in clause:
            variables.add(int(lit) if not lit.startswith("-") else int(lit[1:]))

    variables = sorted(list(variables))
    if variables != list(range(1, len(variables) + 1)):
        return False

    # All checks succeeded
    return True


def bit_matrix_to_clauses(bit_matrix: np.ndarray) -> set:

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

