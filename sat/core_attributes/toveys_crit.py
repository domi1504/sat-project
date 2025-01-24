import numpy as np
from sat.instance.instance import Instance


def is_tovey_satisfied(instance: Instance) -> bool:
    """
    Check whether given instance is a core instance.
    If toveys criterium is met, the instance is trivially satisfiable.

    Toveys criterium:
        Wieder so ein Kombinatorik Ding.
        Formal: Wenn jede Klausel mind. k Literale enthält, und jede Variable max. k mal auftaucht, dann ist Formel
            trivially satisfiable.
            (Andersherum: falles eine Variable gibt, die öfter als k mal auftaucht: kann unsatisfiable sein)
        Ganz durchbissen habe ich das noch nicht.

    :return:
        true <--> core-instance,
        false <--> not core-instance, trivially satisfiable via Toveys cirterium.
    """

    # Length of shortest clause
    k = min([len(clause) for clause in instance.clauses])

    # For every variable: how often does it occur?
    for variable_index in range(instance.num_variables):

        # If #positive_occurences + #negative_occurences > k: Can be unsatisfiable.
        if np.sum(instance.bit_matrix[:, 2 * variable_index]) + np.sum(instance.bit_matrix[:, 2 * variable_index + 1]) > k:
            return True

    return False

