from typing import Callable
from sat.core_attributes.pure_literal import get_pure_literal
from sat.instance.instance import Instance
from sat.modify.assign_and_simplify import assign_and_simplify
from sat.solve.dpll.dpll_node import DPLLNode


def is_satisfiable_dpll(input_instance: Instance, heuristic: Callable[[Instance], int]) -> bool:
    """

    :param input_instance:
    :param heuristic:
    :return:
    """

    # Stack holds tuples of (current_instance, current_assignments)
    stack: list[DPLLNode] = [DPLLNode(input_instance, [])]

    while stack:
        current_node = stack.pop()

        # Check if no clauses left -> satisfiable
        if current_node.instance.num_clauses == 0:
            return True

        # Check for empty clause -> conflict
        if any(len(clause) == 0 for clause in current_node.instance.clauses):
            # Backtrack
            continue

        # Handle unit clauses; unit propagation.
        unit_clause_found = False
        for clause in current_node.instance.clauses:
            if len(clause) == 1:
                # Unit clause found: set variable.
                stack.append(
                    DPLLNode(
                        assign_and_simplify(current_node.instance, {abs(clause[0]): clause[0] > 0}),
                        current_node.assignments.copy() + [clause[0]]
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
                    assign_and_simplify(current_node.instance, {abs(pure_literal): pure_literal > 0}),
                    current_node.assignments.copy() + [pure_literal]
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
                assign_and_simplify(current_node.instance, {abs(literal): not is_positive}),
                current_node.assignments.copy() + [-literal]
            )
        )

        # Try first branch (heuristic's suggested value, stack, so this will get processed first)
        stack.append(
            DPLLNode(
                assign_and_simplify(current_node.instance, {abs(literal): is_positive}),
                current_node.assignments.copy() + [literal]
            )
        )

    # If stack is exhausted without finding a solution
    return False

