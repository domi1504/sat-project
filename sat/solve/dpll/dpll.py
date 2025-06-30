from sat.core_attributes.pure_literal import get_pure_literal
from sat.instance.instance import Instance
from sat.instance.assign_and_simplify import assign_and_simplify
from sat.solve.dpll.dpll_node import DPLLNode
from sat.solve.dpll.heuristics import DPLLHeuristic


def is_satisfiable_dpll(input_instance: Instance, heuristic: DPLLHeuristic) -> bool:
    """
    Determines the satisfiability of a SAT instance using the DPLL (Davis–Putnam–Logemann–Loveland) algorithm.

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

    :param input_instance: The input SAT instance to be checked for satisfiability.
    :param heuristic: A function that selects the next literal to branch on.
    :return: True if the instance is satisfiable, False otherwise.
    """

    # Stack holds tuples of (current_instance, current_assignments)
    stack: list[DPLLNode] = [DPLLNode(input_instance, [])]

    while stack:
        current_node = stack.pop()

        # Check if no clauses left -> satisfiable
        if current_node.instance.num_clauses == 0:
            return True

        # Check for empty clause -> conflict
        if current_node.instance.has_empty_clause():
            # Backtrack
            continue

        # Handle unit clauses; unit propagation.
        unit_clause_found = False
        for clause in current_node.instance.clauses:
            if len(clause) == 1:
                # Unit clause found: set variable.
                stack.append(
                    DPLLNode(
                        assign_and_simplify(
                            current_node.instance, {abs(clause[0]): clause[0] > 0}
                        ),
                        current_node.assignments.copy() + [clause[0]],
                    )
                )
                unit_clause_found = True
                break

        if unit_clause_found:
            # Evaluate after now removed unit clause
            continue

        # Check for pure literals
        pure_literal = get_pure_literal(current_node.instance)
        if pure_literal is not None:
            # Pure literal found: set variable.
            stack.append(
                DPLLNode(
                    assign_and_simplify(
                        current_node.instance, {abs(pure_literal): pure_literal > 0}
                    ),
                    current_node.assignments.copy() + [pure_literal],
                )
            )
            # Evaluate after now removed pure literal
            continue

        # Use heuristic to select next literal
        # If "3" is returned: will first try to set 3 := True, then False.
        # If "-4" is returned: will first try to set 4 := False, then True.
        literal = heuristic(current_node.instance)
        is_positive = literal > 0

        # Try second branch (opposite of heuristic's suggestion, stack, so this will get processed later)
        stack.append(
            DPLLNode(
                assign_and_simplify(
                    current_node.instance, {abs(literal): not is_positive}
                ),
                current_node.assignments.copy() + [-literal],
            )
        )

        # Try first branch (heuristic's suggested value, stack, so this will get processed first)
        stack.append(
            DPLLNode(
                assign_and_simplify(current_node.instance, {abs(literal): is_positive}),
                current_node.assignments.copy() + [literal],
            )
        )

    # If stack is exhausted without finding a solution
    return False
