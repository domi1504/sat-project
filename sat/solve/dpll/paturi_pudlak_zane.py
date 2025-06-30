import math
from sat.instance.instance import Instance
from sat.instance.assign_and_simplify import assign_and_simplify
import numpy as np
import random


def is_satisfiable_paturi_pudlak_zane(
    instance: Instance, error_rate: float = 1e-8
) -> bool:
    """
    Determines satisfiability of a SAT instance using the Paturi-Pudlák-Zane randomized algorithm.

    This algorithm attempts to find a satisfying assignment
    by randomly permuting the variables and assigning values to them in that order.

    For each variable:
      - If the variable appears in a unit clause, it is assigned accordingly.
      - Otherwise, a truth value is chosen at random.

    The number of iterations is calculated to achieve a user-specified error rate ε.
    The probability `p` of randomly guessing a satisfying assignment is estimated as:
        p = 2^(-n * (1 - 1/k))
    where n is the number of variables, and k is the length of the longest clause.
    To reduce the probability of failure to below ε, the algorithm runs for at least:
        ceil(-log(ε) / p) iterations.

    References:
        - Schöning, p. 84 f.
        - Paturi et al.: An improved exponential-time algorithm for k-SAT.
            (2005) - https://doi.org/10.1145/1066100.1066101

    :param instance: The SAT instance to solve.
    :param error_rate: Acceptable error rate (probability of false negative). Lower values increase run time.
    :return: True if a satisfying assignment is found with high probability, False otherwise.
    """

    # Compute necessary number of iterations to achieve desired error_rate
    """
    If instance in k-SAT with n variables, probability p of finding a satisfying assignment:
    p = 2 ** (-n * (1 - (1 / k)))
    To achieve an error_rate of (e ** -c), one has to execute >= c/p iterations
    See Schöning, p.85f.
    """
    k = instance.get_longest_clause_length()
    n = instance.num_variables
    c = -np.log(error_rate)
    p = 2 ** (-n * (1 - (1 / k)))
    nr_iterations = math.ceil(c / p)

    # Create working copy of input instance
    all_variables = list(instance.get_all_variables())

    # Try at max. nr_iterations times
    for _ in range(nr_iterations):

        # Compute random permutation
        variables_random_permutation = list(np.random.permutation(all_variables))

        # Build current (at first partial) assignment
        assignment = {}

        instance_iteration = Instance(instance.clauses.copy())

        # Iterate over permuted variables
        for variable in variables_random_permutation:

            if (variable,) in instance_iteration.clauses:
                # Check if +variable occurs in a unit clause in current instance
                assignment[variable] = True
                instance_iteration = assign_and_simplify(
                    instance_iteration, {variable: True}
                )
            elif (-variable,) in instance_iteration.clauses:
                # Check if -variable occurs in a unit clause in current instance
                assignment[variable] = False
                instance_iteration = assign_and_simplify(
                    instance_iteration, {variable: False}
                )
            else:
                # Choose assignment randomly
                value = random.choice([True, False])
                assignment[variable] = value
                instance_iteration = assign_and_simplify(
                    instance_iteration, {variable: value}
                )

        if not instance_iteration.has_empty_clause():
            # Found satisfying assignment
            return True

    return False
