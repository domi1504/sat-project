from typing import Optional
from sat.instance.instance import Instance


def get_pure_literal(instance: Instance) -> Optional[int]:
    """
    Check if given instance contains pure literals.
    If yes, return the first (arbitrary order) such literal (sic. not variable).
    If no, return none.

    :param instance:
    :return: Literal, not variable. 1-based.
    """

    if instance.num_variables == 0:
        return None

    found_literals = set()
    for clause in instance.clauses:
        for lit in clause:
            found_literals.add(lit)

    for variable in range(1, instance.num_variables):
        assert variable in found_literals or -variable in found_literals
        if -variable not in found_literals:
            return variable
        elif variable not in found_literals:
            return -variable

    return None

