import random
from sat.instance.instance import Instance
from sat.instance.utils import check_assignment, get_unsatisfied_clauses
from sat.solve.local_search.greedy_sat import get_variable_to_flip_gsat


def get_all_variables_of_unsatisfied_clauses(instance: Instance, assignment: dict[int, bool]) -> set[int]:
    unsatisfied_clauses = get_unsatisfied_clauses(instance, assignment)
    occuring_variables = set()
    for clause in unsatisfied_clauses:
        for literal in clause:
            occuring_variables.add(abs(literal))
    return occuring_variables


def is_satisfiable_gsat_with_walk(instance: Instance, max_tries: int = 1000, p: float = 0.55) -> bool:
    """
    From 1994 Selman et al.

    :param instance:
    :param max_tries:
    :return:
    """

    all_variables = list(instance.get_all_variables())

    # See original paper ("multiple of #variables")
    max_flips = len(all_variables) * 2

    for _ in range(max_tries):

        # Restart: New assignment chosen u.a.r.
        assignment = {variable: random.choice([True, False]) for variable in all_variables}

        for __ in range(max_flips):

            # Check if assignments is satisfying assignment
            if check_assignment(instance, assignment):
                return True

            if random.uniform(0, 1) < p:
                # Select a variable at random from all vars occuring in an unsatisfied clause
                variables_to_choose_from = get_all_variables_of_unsatisfied_clauses(instance, assignment)
                selected_variable = random.choice(tuple(variables_to_choose_from))
            else:
                # Use standard GSAT procedure
                selected_variable = get_variable_to_flip_gsat(instance, assignment)

            # Flip literal in assignment
            assignment[selected_variable] = not assignment[selected_variable]

    return False

