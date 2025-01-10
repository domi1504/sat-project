import numpy as np
from sat.instance.instance import Instance


"""
Bit-Matrix
E.g.
(x1 or x2) and (!x2 or x3)
===
101000
000110
"""


def syntax_check_bit_matrix(matrix: str):

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

    if not syntax_check_bit_matrix(matrix):
        raise Exception("Bit matrix syntax check failed")

    lines = matrix.split("\n")

    nr_clauses = len(lines)
    nr_vars = len(lines[0]) // 2

    arr = np.zeros([nr_clauses, nr_vars * 2], dtype=np.uint8)
    for line_count in range(nr_clauses):
        for char_count in range(nr_vars * 2):
            arr[line_count, char_count] = int(lines[line_count][char_count])

    return Instance(arr)


def write_bit_matrix(instance: Instance) -> str:
    lines = ""
    for row in instance.bit_matrix:
        lines += str(row).replace(" ", "").replace("[", "").replace("]", "")
        lines += "\n"
    return lines

