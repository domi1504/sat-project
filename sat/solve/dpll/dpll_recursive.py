from typing import Callable
from sat.core_attributes.pure_literal import get_pure_literal
from sat.instance.instance import Instance
from sat.modify.assign_and_simplify import assign_and_simplify


def is_satisfiable_dpll_recursive(instance: Instance, heuristic: Callable[[Instance], int]) -> bool:
    """

    :param instance:
    :param heuristic:
    :return:
    """

    # Check if clauses left
    if len(instance.clauses) == 0:
        return True

    # Check for empty clause
    if any(len(clause) == 0 for clause in instance.clauses):
        return False

    # Check for unit clauses; unit propagation.
    for clause in instance.clauses:
        if len(clause) == 1:
            # Found unit clause: Fulfill literal and simplify instance
            return is_satisfiable_dpll_recursive(assign_and_simplify(instance, {abs(clause[0]): clause[0] > 0}), heuristic)

    # Check for pure literals
    pure_literal = get_pure_literal(instance)
    if pure_literal is not None:
        return is_satisfiable_dpll_recursive(assign_and_simplify(instance, {abs(pure_literal): pure_literal > 0}), heuristic)

    # Use heuristic to select next literal
    # If "3" is returned: will first try to set 3 := True, then False.
    # If "-4" is returned: will first try to set 4 := False, then True.
    literal = heuristic(instance)
    is_positive = literal > 0

    if is_satisfiable_dpll_recursive(assign_and_simplify(instance, {abs(literal): is_positive}), heuristic):
        return True

    return is_satisfiable_dpll_recursive(assign_and_simplify(instance, {abs(literal): not is_positive}), heuristic)

