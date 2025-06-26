from copy import copy

from sat.instance.instance import Instance


def check_clause(clause: tuple[int, ...], assignment: dict[int, bool]) -> bool:
    for literal in clause:
        if abs(literal) not in assignment:
            break
        if assignment[abs(literal)] == (literal > 0):
            return True
    return False


def check_assignment(instance: Instance, assignment: dict[int, bool]) -> bool:
    """

    :param instance:
    :param assignment:
    :return:
    """
    for clause in instance.clauses:
        if not check_clause(clause, assignment):
            return False
    return True


def get_number_of_satisfied_clauses(instance: Instance, assignment: dict[int, bool]) -> int:
    """

    :param instance:
    :param assignment:
    :return:
    """
    counter = 0
    for clause in instance.clauses:
        if check_clause(clause, assignment):
            counter += 1
    return counter


def get_unsatisfied_clauses(instance: Instance, assignment: dict[int, bool]) -> list[tuple[int, ...]]:
    """

    :param instance:
    :param assignment:
    :return:
    """

    clauses = []

    for clause in instance.clauses:
        if not check_clause(clause, assignment):
            clauses.append(copy(clause))

    return clauses
