import math
import random
import numpy as np
from sat.instance.instance import Instance
from sat.solve.local_search.search_hamming_ball import search_hamming_ball


def is_satisfiable_random_local_search(instance: Instance, error_rate: float) -> bool:
    """
    Determines satisfiability using a randomized local search with bounded error probability.

    This method performs multiple iterations of random local search. In each iteration:
    - A random initial assignment is generated uniformly at random.
    - A search is performed within a Hamming ball of radius δ·n (δ = 1/4) around the assignment.

    The number of iterations is computed to ensure that the overall error probability does not exceed
    the given error_rate.

    Reference:
        - Schöning, p.97 f

    :param instance: A SAT instance to be checked for satisfiability.
    :param error_rate: The maximum acceptable probability of failure (i.e., returning False when the instance is satisfiable).
    :return: True if a satisfying assignment is found within the defined number of iterations, False otherwise.
    """

    # Compute necessary number of iterations to fulfill desired error_rate
    """
    To reach error_rate er:
    er = e ^ -c
    t = (c * 2 ^ n) / (sum i over 0 to delta * n: n choose i)
    See Schöning p.98.
    """
    delta = 0.25
    n = instance.num_variables
    c = -np.log(error_rate)
    limit = int(math.ceil(delta * n))
    numerator = c * (2**n)
    denominator = sum(math.comb(n, i) for i in range(limit + 1))
    nr_iterations = int(math.ceil(numerator / denominator))

    all_variables = instance.get_all_variables()

    for _ in range(nr_iterations):

        # Start with random assignment
        assignment = {
            variable: random.choice([True, False]) for variable in all_variables
        }

        # Search through hamming ball with radius r
        if search_hamming_ball(instance, assignment, int(math.ceil(n * delta))):
            return True

    return False
