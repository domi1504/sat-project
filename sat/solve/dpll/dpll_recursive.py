from sat.core_attributes.pure_literal import get_pure_literal
from sat.instance.instance import Instance
from sat.instance.assign_and_simplify import assign_and_simplify
from sat.solve.dpll.heuristics import DPLLHeuristic


def is_satisfiable_dpll_recursive(instance: Instance, heuristic: DPLLHeuristic) -> bool:
    """
    Determines the satisfiability of a SAT instance using the DPLL (Davis–Putnam–Logemann–Loveland) algorithm.

    Recursive implementation.

    The DPLL procedure performs a backtracking search, enhanced with common SAT solving techniques:
        - Unit propagation: Automatically assigns variables when only one value can satisfy a clause.
        - Pure literal elimination: Assigns variables that occur with only one polarity.
        - Heuristic-based variable selection: Chooses the next literal to branch on using a given heuristic.

    Branching is done according to the heuristic suggestion. If a literal `3` is returned,
    the algorithm first tries `x3 := True`, then `x3 := False`. If `-4` is returned, it first
    tries `x4 := False`, then `x4 := True`.

    References:
        - Schöning, p. 79 f.
        - Biere et al.: Handbook of Satisfiability, Chapter 3.5.

    :param instance: The input SAT instance to be checked for satisfiability.
    :param heuristic: A function that selects the next literal to branch on.
    :return: True if the instance is satisfiable, False otherwise.
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

