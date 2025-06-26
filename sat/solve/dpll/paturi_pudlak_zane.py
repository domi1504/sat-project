import math

from sat.instance.instance import Instance
from sat.instance.assign_and_simplify import assign_and_simplify
import numpy as np
import random


def is_satisfiable_paturi_pudlak_zane(instance: Instance, error_rate: float = 1e-8) -> bool:
    """

    :param instance:
    :param error_rate:
    :return:
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
                instance_iteration = assign_and_simplify(instance_iteration, {variable: True})
            elif (-variable,) in instance_iteration.clauses:
                # Check if -variable occurs in a unit clause in current instance
                assignment[variable] = False
                instance_iteration = assign_and_simplify(instance_iteration, {variable: False})
            else:
                # Choose assignment randomly
                value = random.choice([True, False])
                assignment[variable] = value
                instance_iteration = assign_and_simplify(instance_iteration, {variable: value})

        if not instance_iteration.has_empty_clause():
            # Found satisfying assignment
            return True

    return False

