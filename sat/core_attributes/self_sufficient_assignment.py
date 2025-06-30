from sat.instance.instance import Instance

"""
Referenz: Schöning.
"""


def is_self_sufficient_assignment(
    instance: Instance, assignment: dict[int, bool]
) -> bool:
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
