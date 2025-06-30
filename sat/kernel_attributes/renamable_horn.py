from sat.instance.instance import Instance
from sat.solve.two_sat import is_satisfiable_2_sat


def is_renamable_horn(instance: Instance):
    """
    Check whether the given CNF instance is renamable Horn instance.

    A formula is renamable Horn if it can be transformed into a Horn formula by
    flipping the polarity of some variables. If that is the case, satisfiability can be checked in polynomial time.

    Reference:
        Schöning, p.73 f.

    :param instance:
        A CNF SAT instance to check for renamable Horn property.

    :return:
        True if the instance is renamable Horn, False otherwise.
    """

    # Build check instance F*
    clauses_check: list[tuple[int, ...]] = []

    for clause in instance.clauses:

        # Get all combinations of literals
        for i in range(len(clause) - 1):
            for j in range(i + 1, len(clause)):

                # Add to clauses_check if not inside yet
                a, b = clause[i], clause[j]
                if not (a, b) in clauses_check and (b, a) not in clauses_check:
                    clauses_check.append((a, b))

    instance_check = Instance(clauses_check)

    # Check instance satisfiable <=> instance is renamable horn
    return is_satisfiable_2_sat(instance_check)
