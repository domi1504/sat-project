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


def check_assignment(assignment, instance):
    for row in instance.bit_matrix:
        if not clause_satisfied(assignment, row):
            return False
    return True


def is_satisfiable_brute_force(instance: Instance) -> bool:

    for assignment_index in range(2 ** instance.num_variables):
        assignment = format(assignment_index, f'0{instance.num_variables}b')
        if check_assignment(assignment, instance):
            return True

    return False

