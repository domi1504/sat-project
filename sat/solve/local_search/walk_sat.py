import random
from sat.instance.instance import Instance
from sat.instance.utils import check_assignment, get_unsatisfied_clauses, get_number_of_satisfied_clauses


def get_variable_to_flip_wsat(instance: Instance, assignment: dict[int, bool], clause: tuple) -> int:
    """
    Selects the variable within the given unsatisfied clause that, if flipped,
    maximizes the number of satisfied clauses in the SAT instance.

    If multiple variables achieve the same best score, one is chosen at random.

    :param instance: The SAT instance.
    :param assignment: The current variable assignment.
    :param clause: An unsatisfied clause represented as a tuple of literals.
    :return: The variable index (positive integer) to flip.
    """

    candidates = list(abs(lit) for lit in clause)

    best_score = -1
    best_variables = [-1]
    for variable in candidates:
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
        return best_variables[
            random.randint(0, len(best_variables) - 1)
        ]
    else:
        # Return the only one
        return best_variables[0]


def is_satisfiable_wsat(instance: Instance, max_tries: int = 1000, p: float = 0.55) -> bool:
    """
    Attempts to solve the SAT instance using the WalkSAT algorithm.

    References:
        - Schöning, p.111 f.
        - Selman, Kautz, Cohen: Noise Strategies for Improving Local Search.
            (1994) - Proceedings of the Twelfth National Conference on Artificial Intelligence (Vol. 1), p. 337 - 343.
        Kommentar zu Schöning: sein Zusatz
            "falls es Variable gibt, die geflippt werden kann, ohne das andere klauseln falsch werden, [...]"
            hab ich im Paper nicht gefunden; deswegen hier erstmal weggelassen.

    :param instance: The SAT instance to solve.
    :param max_tries: Maximum number of random restarts (default 1000).
    :param p: Probability of making a random flip (default 0.55).
    :return: True if a satisfying assignment is found, False otherwise.
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

            # Select unsatisfied clause at random
            unsatisfied_clauses = get_unsatisfied_clauses(instance, assignment)
            selected_clause = unsatisfied_clauses[
                random.randint(0, len(unsatisfied_clauses) - 1)
            ]

            if random.uniform(0, 1) < p:
                # Select one variable of the unsatisfied clause at random
                selected_variable = random.choice(selected_clause)
                selected_variable = abs(selected_variable)
            else:
                # Use standard GSAT procedure
                selected_variable = get_variable_to_flip_wsat(instance, assignment, selected_clause)

            # Flip literal in assignment
            assignment[selected_variable] = not assignment[selected_variable]

    return False

