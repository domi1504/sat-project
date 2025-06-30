from sat.instance.instance import Instance
from sat.solve.two_sat import is_satisfiable_2_sat

"""
Referenz: Schöning.
"""


def is_renamable_horn(instance: Instance):

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
