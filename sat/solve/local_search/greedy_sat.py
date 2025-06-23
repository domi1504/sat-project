import random
from sat.instance.instance import Instance
from sat.instance.utils.utils import check_assignment, get_unsatisfied_clauses, get_number_of_satisfied_clauses


def get_variable_to_flip_gsat(instance: Instance, assignment: dict[int, bool]) -> int:
    """
    Select variable to flip greedily:
    Select variable that, when value flipped, maximizes the number of satisfied clauses.

    :param instance:
    :param assignment:
    :return:
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
        return  best_variables[
            random.randint(0, len(best_variables) - 1)
        ]
    else:
        # Return the only one
        return best_variables[0]


def is_satisfiable_gsat(instance: Instance, max_tries: int = 1000) -> bool:
    """

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

            # Select next variable to flip greedily
            selected_variable = get_variable_to_flip_gsat(instance, assignment)

            # Flip literal in assignment
            assignment[selected_variable] = not assignment[selected_variable]

    return False

