from sat.core_attributes.self_sufficient_assignment import is_self_sufficient_assignment
from sat.instance.instance import Instance
from sat.instance.assign_and_simplify import assign_and_simplify


def is_satisfiable_monien_speckenmeyer(
    instance: Instance, with_self_sufficient_assignments_check: bool
) -> bool:
    """
    Determines the satisfiability of a SAT instance using the Monien-Speckenmeyer splitting algorithm.

    This recursive algorithm attempts to reduce the instance by selecting a clause of minimal length `k`
    and exploring `k` different partial assignments:
    - For each literal in the clause, assume all previous literals in the clause are set to `False`
      and the current literal to `True`, then recursively check satisfiability of the simplified instance.

    Optionally, the function can also check for "self-sufficient assignments" (autarke Belegungen), a refinement used
    in extensions of Schöning-type algorithms. If enabled, the function first tries to find a partial assignment that
    satisfies part of the formula independently and simplifies the instance accordingly.

    References:
        - Schöning, p. 81 f.
        - Monien, Speckenmeyer: Solving satisfiability in less than 2^n steps
            (1985) - https://doi.org/10.1016/0166-218X(85)90050-2

    :param instance: The SAT instance to be solved.
    :param with_self_sufficient_assignments_check: If True, will check for and apply self-sufficient assignments
                                                   before proceeding with the basic recursive search.
    :return: True if the instance is satisfiable, False otherwise.
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

    if with_self_sufficient_assignments_check:
        for i in range(k):

            # Assume clause is: (1, -4, 8, 11, -12)
            # Create assignment turning all literals until i to False, and i to True
            # e.g. i = 3
            # {1: False, -4: False, 8: True}
            assignments = {}
            for j in range(i):
                assignments[abs(clause[j])] = clause[j] < 0
            assignments[abs(clause[i])] = clause[i] > 0

            if is_self_sufficient_assignment(instance, assignments):
                return is_satisfiable_monien_speckenmeyer(
                    assign_and_simplify(instance, assignments),
                    with_self_sufficient_assignments_check,
                )

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

        if is_satisfiable_monien_speckenmeyer(
            assign_and_simplify(instance, assignments),
            with_self_sufficient_assignments_check,
        ):
            return True

    return False
