import numpy as np
from sat.instance.instance import Instance


def is_biathlet_satisfied(instance: Instance) -> bool:
    """
    Determine whether the given SAT instance can be unsatisfiable based on a combinatorial criterion
    referred to as the "Biathlet property."

    This property compares the total number of assignments excluded by the clauses ("shots")
    to the total number of possible assignments. If the excluded assignments cover the entire space,
    the instance may be unsatisfiable.

    Reference:
        Schöning, p. 32 ff.

    :param instance:
        The SAT instance to evaluate.

    :return:
        True  --> The instance may be unsatisfiable (kernel instance).
        False --> The instance is trivially satisfiable.
    """

    # Number of possible assignments
    nr_of_targets = 2**instance.num_variables

    nr_of_shots = 0
    for clause in instance.get_bit_matrix():
        # 2 ^ (|V| - k), k = nr of literals in the clause
        nr_of_shots += 2 ** (instance.num_variables - np.sum(clause))

    return nr_of_shots >= nr_of_targets
