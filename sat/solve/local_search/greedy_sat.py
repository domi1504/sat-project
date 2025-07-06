import random
from sat.instance.instance import Instance
from sat.instance.utils import check_assignment, get_number_of_satisfied_clauses


def get_variable_to_flip_gsat(instance: Instance, assignment: dict[int, bool]) -> int:
    """
    Selects the next variable to flip in the GSAT (Greedy SAT) local search algorithm.

    This function evaluates all possible single-variable flips and chooses the one that results
    in the greatest increase in the number of satisfied clauses. If multiple variables yield the
    same best score, one is selected uniformly at random.

    :param instance: The SAT instance to evaluate.
    :param assignment: The current variable assignment.
    :return: The variable to flip, selected greedily.
    """

    all_variables = list(instance.get_all_variables())

    best_score = -1
    best_variables = [-1]
    for variable in all_variables:
        assignment_copy = assignment.copy()
        assignment_copy[variable] = not assignment_copy[variable]
        score = get_number_of_satisfied_clauses(instance, assignment_copy)
        if score > best_score:
            best_score = get_number_of_satisfied_clauses(instance, assignment_copy)
            best_variables = [variable]
        elif score == best_score:
            best_variables.append(variable)

    assert best_variables != [-1]

    if len(best_variables) > 1:
        # Return one at random
        return best_variables[random.randint(0, len(best_variables) - 1)]
    else:
        # Return the only one
        return best_variables[0]


def is_satisfiable_gsat(instance: Instance, max_tries: int = 1000) -> tuple[bool, int]:
    """
    Determines the satisfiability of a SAT instance using the GSAT (Greedy SAT) algorithm.

    GSAT is a local search algorithm that repeatedly starts from a random assignment and iteratively
    flips variables to maximize the number of satisfied clauses. The process is restarted multiple
    times to avoid local optima.

    Reference:
        - Schöning, p.111 f.
        - Selman, Levesque, Mitchell: A New Method for Solving Hard Satisfiability Problems.
            (1992) - Proceedings of the Tenth National Conference on Artificial Intelligence, p.440 – 446

    :param instance: The SAT instance to solve.
    :param max_tries: Number of random restarts (default: 1000).
    :return: A tuple containing a boolean indicating whether a satisfying was found,
             and the number of iterations performed during the search.
    """

    all_variables = list(instance.get_all_variables())

    # See original paper ("multiple of #variables")
    max_flips = len(all_variables) * 2

    checked_assignment_counter = 0

    for _ in range(1, max_tries + 1):

        # Restart: New assignment chosen u.a.r.
        assignment = {
            variable: random.choice([True, False]) for variable in all_variables
        }

        for __ in range(max_flips):
            checked_assignment_counter += 1

            # Check if assignments is satisfying assignment
            if check_assignment(instance, assignment):
                return True, checked_assignment_counter

            # Select next variable to flip greedily
            selected_variable = get_variable_to_flip_gsat(instance, assignment)

            # Flip literal in assignment
            assignment[selected_variable] = not assignment[selected_variable]

    return False, checked_assignment_counter
