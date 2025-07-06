import math
import random
import numpy as np
from sat.instance.instance import Instance
from sat.instance.utils import check_assignment, get_unsatisfied_clauses


def is_satisfiable_schoening(instance: Instance, error_rate: float = 1e-8) -> tuple[bool, int]:
    """
    Determines the satisfiability of a SAT instance using Schöning's probabilistic local search algorithm.

    This algorithm randomly samples initial assignments and performs local search by flipping variables
    in randomly chosen unsatisfied clauses. The number of restarts is determined based on the desired
    error rate.

    References:
        - Schöning, p.102 f.
        - Schöning: A Probabilistic Algorithm for k-SAT and Constraint Satisfaction Problems
            (1999) - https://doi.org/10.1109/SFFCS.1999.814612

    :param instance: The SAT instance to solve.
    :param error_rate: Desired upper bound on the failure probability (default is 1e-8).
    :return: A tuple containing a boolean indicating whether a satisfying assignment was found,
             and the number of iterations performed during the search.
    :return: True if a satisfying assignment is found , False otherwise.
    """

    k = instance.get_longest_clause_length()
    inversed_prob = 2 * (1 - (1 / k))
    c = -np.log(error_rate)
    number_iterations = math.ceil(c * (inversed_prob**instance.num_variables))

    all_variables = list(instance.get_all_variables())

    check_count = 0

    for _ in range(number_iterations):

        # (Re)start: New assignment chosen u.a.r.
        assignment = {}
        for variable in all_variables:
            assignment[variable] = random.choice([True, False])

        for __ in range(instance.num_variables):
            check_count += 1

            # Check if assignments is satisfying assignment
            if check_assignment(instance, assignment):
                return True, check_count

            # Choose one unsatisfied clause u.a.r
            unsatisfied_clauses = get_unsatisfied_clauses(instance, assignment)
            selected_clause = unsatisfied_clauses[
                random.randint(0, len(unsatisfied_clauses) - 1)
            ]

            # Choose one variable u.a.r
            selected_variable = abs(
                selected_clause[random.randint(0, len(selected_clause) - 1)]
            )

            # Flip literal in assignment
            assignment[selected_variable] = not assignment[selected_variable]

    return False, check_count

