from sat.instance.instance import Instance
from sat.instance.assign_and_simplify import assign_and_simplify


def is_self_sufficient_assignment(
    instance: Instance, assignment: dict[int, bool]
) -> bool:
    """
    Determine whether a given assignment is self-sufficient ("autark").

    According to Schöning's definition, an assignment is self-sufficient if every clause that is
    "touched" by it (i.e., contains at least one of the assigned variables) is satisfied by the assignment.

    In other words, the assignment must satisfy all clauses that involve any of the assigned variables.

    :param instance: (Instance) A SAT instance containing clauses over variables.
    :param assignment: (dict[int, bool]) A partial assignment mapping variable indices to Boolean values.

    :return:
        bool:
            True  --> The assignment is self-sufficient (autark).
            False --> There exists at least one touched clause that is not satisfied by the assignment.
    """

    """
    Given an instance and an assignment, check whether given assignment is a self-sufficient assignment.
    (Schöning: "autark")

    Meaning: Every clause that is "touched" (contains a variable that the assignment also contains), is satisfied
        by the assignment.

    :param instance:
    :param assignment:
    :return:
    """

    assigned_variables = list(assignment.keys())
    true_literals = list(
        (variable if value else -variable) for (variable, value) in assignment.items()
    )

    for clause in instance.clauses:
        if any((abs(lit) in assigned_variables) for lit in clause):
            # Clause is "touched" by assignment

            # Check if assignment does NOT satisfy clause (= none of the assigned variables appear in the correct form)
            if not any((true_literal in clause) for true_literal in true_literals):
                return False

    # All touched clauses satisfied
    return True


def is_satisfiable_monien_speckenmeyer_recursive(
    instance: Instance, with_self_sufficient_assignments_check: bool
) -> bool:
    """
    Determines the satisfiability of a SAT instance using the Monien-Speckenmeyer splitting algorithm.

    This recursive algorithm attempts to reduce the instance by selecting a clause of minimal length `k`
    and exploring `k` different partial assignments:
    - For each literal in the clause, assume all previous literals in the clause are set to `False`
      and the current literal to `True`, then recursively check satisfiability of the simplified instance.

    If enabled, the function optionally applies a pre-processing step that detects
    self-sufficient ("autark") partial assignments. When such an assignment is found, the instance is
    simplified accordingly before recursive search continues.

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
                return is_satisfiable_monien_speckenmeyer_recursive(
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

        if is_satisfiable_monien_speckenmeyer_recursive(
            assign_and_simplify(instance, assignments),
            with_self_sufficient_assignments_check,
        ):
            return True

    return False
