import numpy as np
from sat.instance.instance import Instance


def is_2_sat(instance: Instance) -> bool:
    """
    Check whether given formula is a core instance.
    If it is a 2-SAT instance, it is trivially solvable.

    2-SAT: all clauses have length 2.

    :return:
        true <--> 2-sat-instance, thus not core,
        false <--> core-instance.
    """

    # Length of longest clause
    k = np.max([np.sum(clause) for clause in instance.bit_matrix])
    return k == 2
