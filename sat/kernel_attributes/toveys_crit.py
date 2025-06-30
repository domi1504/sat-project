import numpy as np
from sat.instance.instance import Instance


def is_tovey_satisfied(instance: Instance) -> bool:
    """
    Determine whether an instance satisfies Tovey's criterion for satisfiability.

    Tovey's criterion states that a CNF formula is satisfiable if:
        - Every clause contains at least k literals, and
        - No variable appears (positively or negatively) in more than k clauses,
          where k is the size of the smallest clause.

    Reference:
        Schöning, p.36

    :param instance: (Instance): A SAT instance containing clauses and variables.

    :return:
        bool:
            True  --> The instance is trivially satisfiable according to Tovey's criterion.
            False --> The instance may be unsatisfiable (violates Tovey's criterion; potential kernel instance).
    """

    # Length of shortest clause
    k = min([len(clause) for clause in instance.clauses])

    # For every variable: how often does it occur?
    for variable_index in range(instance.num_variables):

        # If #positive_occurences + #negative_occurences > k: Can be unsatisfiable.
        if (
            np.sum(instance.get_bit_matrix()[:, 2 * variable_index])
            + np.sum(instance.get_bit_matrix()[:, 2 * variable_index + 1])
            > k
        ):
            return True

    return False
