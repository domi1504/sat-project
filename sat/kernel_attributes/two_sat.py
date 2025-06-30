from sat.instance.instance import Instance


def is_2_sat(instance: Instance) -> bool:
    """
    Check whether given formula is a 2-SAT instance.
    If it is a 2-SAT instance, it is solvable in polynomial time.

    :return: Whether given instance is a 2-SAT instance
    """

    # Length of longest clause
    k = max([len(clause) for clause in instance.clauses])
    return k == 2
