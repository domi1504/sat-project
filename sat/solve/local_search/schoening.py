import math
import random

import numpy as np

from sat.instance.instance import Instance
from sat.instance.utils import check_assignment, get_unsatisfied_clauses


def is_satisfiable_schoening(instance: Instance, error_rate: float = 1e-8) -> bool:
    """

    :param instance:
    :param error_rate:
    :return:
    """

    # See p.105 in Schoening.
    k = instance.get_longest_clause_length()
    inversed_prob = 2 * (1 - (1 / k))
    c = -np.log(error_rate)
    number_iterations = math.ceil(c * (inversed_prob ** instance.num_variables))

    all_variables = list(instance.get_all_variables())

    for _ in range(number_iterations):

        # (Re)start: New assignment chosen u.a.r.
        assignment = {}
        for variable in all_variables:
            assignment[variable] = random.choice([True, False])

        for __ in range(instance.num_variables):

            # Check if assignments is satisfying assignment
            if check_assignment(instance, assignment):
                return True

            # Choose one unsatisfied clause u.a.r
            unsatisfied_clauses = get_unsatisfied_clauses(instance, assignment)
            selected_clause = unsatisfied_clauses[
                random.randint(0, len(unsatisfied_clauses) - 1)
            ]

            # Choose one variable u.a.r
            selected_variable = abs(
                selected_clause[
                    random.randint(0, len(selected_clause) - 1)
                ]
            )

            # Flip literal in assignment
            assignment[selected_variable] = not assignment[selected_variable]

    return False

