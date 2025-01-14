import numpy as np
from sat.instance.instance import Instance


def is_biathlet_satisfied(instance: Instance) -> bool:
    """
    Check whether given SAT-instance can be unsatisfiable.
    "Biathlet-Eigenschaft".

    :param instance:
    :return:
        true <--> core-instance,
        false <--> trivially satisfiable
    """

    # Number of possible assignments
    nr_of_targets = 2 ** instance.nr_vars()

    nr_of_shots = 0
    for clause in instance.bit_matrix:
        # 2 ^ (|V| - k), k = nr of literals in the clause
        nr_of_shots += (2 ** (instance.nr_vars() - np.sum(clause)))

    return nr_of_shots >= nr_of_targets

