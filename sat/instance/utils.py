from copy import copy
from sat.instance.instance import Instance


def is_clause_satisfied(clause: tuple[int, ...], assignment: dict[int, bool]) -> bool:
    """
    Checks whether a given clause is satisfied under a variable assignment.

    :param clause: A clause represented as a tuple of integers, where a positive
                   integer represents a variable and a negative integer its negation.
    :param assignment: A mapping from variable indices to boolean values.
    :return: True if the clause is satisfied under the assignment, False otherwise.
    """
    for literal in clause:
        if abs(literal) not in assignment:
            break
        if assignment[abs(literal)] == (literal > 0):
            return True
    return False


def check_assignment(instance: Instance, assignment: dict[int, bool]) -> bool:
    """
    Checks whether a given variable assignment satisfies all clauses in a SAT instance.

    :param instance: A SAT instance containing a list of clauses.
    :param assignment: A mapping from variable indices to boolean values.
    :return: True if all clauses are satisfied under the assignment, False otherwise.
    """
    for clause in instance.clauses:
        if not is_clause_satisfied(clause, assignment):
            return False
    return True


def get_number_of_satisfied_clauses(instance: Instance, assignment: dict[int, bool]) -> int:
    """
    Counts the number of clauses satisfied by a given variable assignment in a SAT instance.

    :param instance: A SAT instance containing a list of clauses.
    :param assignment: A mapping from variable indices to boolean values.
    :return: The number of clauses satisfied under the given assignment.
    """
    counter = 0
    for clause in instance.clauses:
        if is_clause_satisfied(clause, assignment):
            counter += 1
    return counter


def get_unsatisfied_clauses(instance: Instance, assignment: dict[int, bool]) -> list[tuple[int, ...]]:
    """
    Returns a list of clauses that are not satisfied under the given variable assignment.

    :param instance: A SAT instance containing a list of clauses.
    :param assignment: A mapping from variable indices to boolean values.
    :return: A list of clauses that are not satisfied under the assignment.
    """

    clauses = []

    for clause in instance.clauses:
        if not is_clause_satisfied(clause, assignment):
            clauses.append(copy(clause))

    return clauses
