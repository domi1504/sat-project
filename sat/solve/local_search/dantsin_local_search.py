import math
import random
import numpy as np
from sat.instance.instance import Instance
from sat.solve.local_search.cover_code import generate_cover_code
from sat.solve.local_search.search_hamming_ball import search_hamming_ball



def is_satisfiable_dantsin_local_search(instance: Instance) -> bool:
    """
    Apply the dantsin local search algorithm.

    :param instance:
    :return:
    """

    delta = 0.25
    cover_code = generate_cover_code(instance.num_variables, delta)

    for assignment in cover_code:

        # Search through hamming ball with radius delta * n
        if search_hamming_ball(instance, assignment, int(instance.num_variables * delta)):
            return True

    return False

