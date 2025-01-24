from sat.instance.instance import Instance, get_instance_from_clauses


def assign_and_simplify(instance: Instance, variable: int, value: bool) -> Instance:
    """
    Assign a value to a variable at specified index and simplify the resulting clauses.
    Return a new instance.

    :param instance:
    :param variable: 1-based
    :param value:
    :return:
    """
    assert 1 <= variable <= instance.num_variables

    literal_true = variable if value else -variable
    literal_false = -variable if value else variable

    # Remove clauses containing the satisfied literal
    # (Convert clauses from tuples to lists for easier deletion of not-satisfied literal)
    clauses = list(list(clause) for clause in instance.clauses if not literal_true in clause)

    # Remove literal from clauses containing the not-satisfied literal
    for clause in clauses:
        if literal_false in clause:
            clause.remove(literal_false)

    clauses = set(tuple(clause) for clause in clauses)

    return get_instance_from_clauses(clauses)

