import numpy as np
from sat.instance.instance import Instance, get_instance_from_bit_matrix

"""
Bit Matrix Format Parser and Serializer for SAT Instances

This module provides functionality to work with SAT instances represented in
a compact binary matrix form. Each clause is encoded as a binary row, where
each variable is represented by two bits:
    - One bit for its positive literal
    - One bit for its negated literal

Example Bit Matrix Representation:
    (x1 ∨ x2) ∧ (¬x2 ∨ x3)

    101000
    000110

Each row corresponds to a clause, with two columns per variable.
"""


def syntax_check_bit_matrix(matrix: str):
    """
    Checks if a given string representation is a syntactically valid bit matrix.

    A valid bit matrix string must:
    - Contain only '0', '1', and newline characters
    - Have all lines of equal length
    - Have an even number of characters per line (2 per variable)
    - Contain only valid binary digits (no other characters)

    :param matrix: String representing the bit matrix.
    :return: True if the syntax is valid; False otherwise.
    """

    # Check for valid chars
    for c in matrix:
        if c not in ['0', '1', '\n']:
            return False

    # Last line empty
    lines = matrix.split("\n")

    # Check all lines are bit strings of same even length
    for l in lines:
        if len(l) % 2 != 0:
            return False
        if len(l) != len(lines[0]):
            return False
        if len(l) != l.count('0') + l.count('1'):
            return False

    return True


def parse_bit_matrix(matrix: str) -> Instance:
    """
    Parses a string representation of a bit matrix into an `Instance` object.

    First, it validates the syntax of the input string using `syntax_check_bit_matrix`.
    Then it converts each line of binary digits into a row of a NumPy array,
    and finally transforms the bit matrix into an `Instance` of clauses.

    :param matrix: String representing the bit matrix (one row per line).
    :return: Instance object corresponding to the parsed bit matrix.
    :raises Exception: If the input string does not pass the syntax check.
    """

    if not syntax_check_bit_matrix(matrix):
        raise Exception("Bit matrix syntax check failed")

    lines = matrix.split("\n")

    nr_clauses = len(lines)
    nr_vars = len(lines[0]) // 2

    bit_matrix = np.zeros([nr_clauses, nr_vars * 2], dtype=np.uint8)
    for line_count in range(nr_clauses):
        for char_count in range(nr_vars * 2):
            bit_matrix[line_count, char_count] = int(lines[line_count][char_count])

    return get_instance_from_bit_matrix(bit_matrix)


def write_bit_matrix(instance: Instance) -> str:
    """
    Serializes the bit matrix of an `Instance` object into a string.

    Each clause is represented as a row of binary digits (0 or 1),
    with one clause per line.

    Example output:
        101000
        000110

    :param instance: An `Instance` object containing SAT clauses.
    :return: A string representation of the instance's bit matrix.
    """

    lines = ""
    for row in instance.get_bit_matrix():
        lines += str(row).replace(" ", "").replace("[", "").replace("]", "")
        lines += "\n"
    return lines

