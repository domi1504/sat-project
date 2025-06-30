from typing import Optional
from sat.instance.instance import Instance


def get_pure_literal(instance: Instance) -> Optional[int]:
    """
    Check whether the given instance contains any pure literals.

    A pure literal is a literal that appears with only one polarity across all clauses
    (i.e., either only positive or only negative, but not both). This function returns
    the first such literal found, if any.

    :param instance:
        A SAT instance containing a set of clauses over literals.

    :return:
        A pure literal if one exists (positive or negative). Literal, not variable. 1-based.
        Returns None if no pure literal is found.
    """

    if instance.num_variables == 0:
        return None

    found_literals = set()
    for clause in instance.clauses:
        for lit in clause:
            found_literals.add(lit)

    for variable in range(1, instance.num_variables):
        if -variable not in found_literals and variable in found_literals:
            return variable
        elif variable not in found_literals and -variable in found_literals:
            return -variable

    return None
