
import math
import random

import numpy as np

from sat.instance.instance import Instance
from sat.instance.utils.utils import check_assignment, get_unsatisfied_clauses


def search_hamming_ball(instance: Instance, assignment: dict[int, bool], radius: int) -> bool:
    """

    :param instance:
    :param assignment:
    :param radius:
    :return:
    """
    assert len(assignment) == instance.num_variables

    if check_assignment(instance, assignment):
        # Found satisfying assignment
        return True

    if radius == 0:
        # Search space exhausted
        return False

    # Pick one unsatisfied clause randomly
    unsatisfied_clauses = get_unsatisfied_clauses(instance, assignment)
    selected_clause = unsatisfied_clauses[
        random.randint(0, len(unsatisfied_clauses) - 1)
    ]

    # Try to flip every contained literal, search recursively with decreased radius
    for literal in selected_clause:
        if search_hamming_ball(
            instance,
            {**assignment, abs(literal): not assignment[abs(literal)]},
            radius - 1
        ):
            return True

    return False



