import math
import random
import numpy as np
from sat.instance.instance import Instance
from sat.solve.local_search.search_hamming_ball import search_hamming_ball


def is_satisfiable_random_local_search(instance: Instance, error_rate: float) -> bool:
    """
    Apply random local search.
    Iterate for t times:
        start with initial assignment u.a.r.
        search hamming ball with radius r (1/4 * n)

    To reach error_rate er:
    er = e ^ -c
    t = (c * 2 ^ n) / (sum i over 0 to delta * n: n choose i)
    See Schöning p.98.

    :param instance:
    :param error_rate:
    :return:
    """

    # Compute necessary number of iterations to fulfill desired error_rate
    delta = 0.25
    n = instance.num_variables
    c = -np.log(error_rate)
    limit = int(math.ceil(delta * n))
    numerator = c * (2 ** n)
    denominator = sum(math.comb(n, i) for i in range(limit + 1))
    nr_iterations = int(math.ceil(numerator / denominator))

    all_variables = instance.get_all_variables()

    for _ in range(nr_iterations):

        # Start with random assignment
        assignment = {variable: random.choice([True, False]) for variable in all_variables}

        # Search through hamming ball with radius r
        if search_hamming_ball(instance, assignment, int(math.ceil(n * delta))):
            return True

    return False


