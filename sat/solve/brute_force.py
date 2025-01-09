import numpy as np
from sat.instance.instance import Instance


def clause_satisfied(assignment, row):
    one_positions = np.where(row)[0]
    for one_pos in one_positions:
        var_index = one_pos // 2
        necessary_value = '1' if (one_pos % 2 == 0) else '0'
        if assignment[var_index] == necessary_value:
            return True
    return False


def check_assignment(assignment, formula):
    for row in formula.matrix:
        if not clause_satisfied(assignment, row):
            return False
    return True


def is_satisfiable(instance: Instance):

    nr_vars = instance.nr_vars()

    for assignment_index in range(2 ** nr_vars):
        assignment = format(assignment_index, f'0{nr_vars}b')
        if check_assignment(assignment, instance):
            return assignment

    return None


