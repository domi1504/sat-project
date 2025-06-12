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

    clauses = list(tuple(clause) for clause in clauses)
    return Instance(clauses)


def assign_and_simplify_cdcl(instance: Instance, assignments: dict[int, bool], pointers_to_original: list[int]) -> tuple[Instance, list[int]]:
    """
    Assign values to variables at specified indices and simplify the resulting clauses.
    Return a new instance.

    Additionally for cdcl: update the pointers-list of the returned clauses with respect to the original clauses.
        (pointers_to_original[i] <=> index of corresponding clause in original input instance of instance.clauses[i])

    :param instance:
    :param assignments: Dict of form {1: True, 4: False, ...} assigning bool values to specified variables.
        Variables are 1-based.
    :return:
    """
    assert len(pointers_to_original) == instance.num_clauses

    literals_true = list((variable if value else -variable) for (variable, value) in assignments.items())
    literals_false = list((-variable if value else variable) for (variable, value) in assignments.items())

    # Remove clauses containing at least one satisfied literal
    # (Convert clauses from tuples to lists for easier deletion of not-satisfied literal)
    updated_clauses = []
    updated_pointers = []

    for index, clause in enumerate(instance.clauses):
        if any(lit in clause for lit in literals_true):
            # Clause satisfied, remove it
            continue
        updated_clauses.append(list(clause))
        updated_pointers.append(pointers_to_original[index])

    # Remove negated literals from clauses containing the not-satisfied literals
    for clause in updated_clauses:
        for literal_false in literals_false:
            if literal_false in clause:
                clause.remove(literal_false)

    updated_clauses = list(tuple(clause) for clause in updated_clauses)
    return Instance(updated_clauses), updated_pointers

