import numpy as np
from sat.instance.instance import Instance


def is_lll_satisfied(instance: Instance) -> bool:
    """
    Check whether the given SAT instance can be unsatisfiable based on the Lovász Local Lemma (LLL).

    Intuition behind LLL here:
    For a formula to be unsatisfiable, the following must hold for every clause:
        Any assignment that satisfies this clause must still fail to satisfy the entire formula.
        This can only happen if there are enough "dependent" clauses that prevent the formula from being satisfiable.

    Example:
        Consider a clause with exactly k literals (e.g., 3 variables: a, b, c).
        If the formula is unsatisfiable, then all assignments that satisfy this clause are "blocked" by other clauses
        containing overlapping variables.
        There must be enough such clauses to cover all combinations to prevent satisfiability.

    Reference:
        Schöning, p.32 f.

    :param instance:
        The SAT instance to be checked.

    :return:
        True  --> The instance may be unsatisfiable (qualifying to be kernel instance).
        False --> The instance is trivially satisfiable due to the Lovász Local Lemma.
    """

    bit_matrix = instance.get_bit_matrix()

    k = np.sum(bit_matrix[0])
    for clause in bit_matrix:
        if np.sum(clause) != k:
            raise Exception(
                "LLL not applicable, because not every clause has same length k"
            )

    var_occs = np.zeros((bit_matrix.shape[0], bit_matrix.shape[1] // 2), dtype=np.uint8)
    for i in range(var_occs.shape[0]):
        for j in range(var_occs.shape[1]):
            var_occs[i, j] = bit_matrix[i, 2 * j] or bit_matrix[i, 2 * j + 1]

    for i in range(instance.num_clauses):

        associated_counter = 0
        for j in range(instance.num_clauses):

            if i == j:
                continue

            if 2 in (var_occs[i] + var_occs[j]):
                associated_counter += 1

        if associated_counter >= 2 ** (k - 2):
            return True

    return False
