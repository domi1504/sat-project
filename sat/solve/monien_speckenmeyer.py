from sat.instance.instance import Instance
from sat.modify.assign_and_simplify import assign_and_simplify


def is_satisfiable_monien_speckenmeyer(instance: Instance) -> bool:
    """

    :param instance:
    :return:
    """

    # Check if clauses left
    if len(instance.clauses) == 0:
        return True

    # Check for empty clause
    if any(len(clause) == 0 for clause in instance.clauses):
        return False

    # Get size of smallest occurring clause
    k = min(len(clause) for clause in instance.clauses)

    # Get first min-length clause
    clause = next(c for c in instance.clauses if len(c) == k)

    # Start: Try with i = 1, i = 2, ...
    for i in range(k):

        # Assume clause is: (1, -4, 8, 11, -12)
        # Create assignment turning all literals until i to False, and i to True
        # e.g. i = 3
        # {1: False, -4: False, 8: True}
        assignments = {}
        for j in range(i):
            assignments[abs(clause[j])] = clause[j] < 0
        assignments[abs(clause[i])] = clause[i] > 0

        if is_satisfiable_monien_speckenmeyer(assign_and_simplify(instance, assignments)):
            return True

    return False

