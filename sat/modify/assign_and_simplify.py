from sat.instance.instance import Instance


def assign_and_simplify(instance: Instance, assignments: dict[int, bool]) -> Instance:
    """
    Assign values to variables at specified indices and simplify the resulting clauses.
    Return a new instance.

    :param instance:
    :param assignments: Dict of form {1: True, 4: False, ...} assigning bool values to specified variables.
        Variables are 1-based.
    :return:
    """

    literals_true = list((variable if value else -variable) for (variable, value) in assignments.items())
    literals_false = list((-variable if value else variable) for (variable, value) in assignments.items())

    # Remove clauses containing at least one satisfied literal
    # (Convert clauses from tuples to lists for easier deletion of not-satisfied literal)
    clauses = list(list(clause) for clause in instance.clauses if not any(lit in clause for lit in literals_true))

    # Remove negated literals from clauses containing the not-satisfied literals
    for clause in clauses:
        for literal_false in literals_false:
            if literal_false in clause:
                clause.remove(literal_false)

    clauses = set(tuple(clause) for clause in clauses)
    return Instance(clauses)
