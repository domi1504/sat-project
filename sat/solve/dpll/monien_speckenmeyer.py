from sat.instance.instance import Instance
from sat.instance.assign_and_simplify import assign_and_simplify
from sat.solve.dpll.dpll_node import DPLLNode
from sat.solve.dpll.monien_speckenmeyer_recursive import is_self_sufficient_assignment


def is_satisfiable_monien_speckenmeyer(
    input_instance: Instance, with_self_sufficient_assignments_check: bool
) -> tuple[bool, int]:
    """
    Determines whether a given SAT instance is satisfiable using the
    Monien-Speckenmeyer algorithm.

    The algorithm selects a clause of minimal length `k` and explores `k` distinct
    partial assignments. For each literal in the clause, it assumes all previous literals
    are assigned `False` and the current one `True`, then recursively checks satisfiability
    of the simplified instance.

    If enabled, the function optionally applies a pre-processing step that detects
    self-sufficient ("autark") partial assignments. When such an assignment is found, the instance is
    simplified accordingly before recursive search continues.

    References:
        - Schöning, p. 81 f.
        - Monien, Speckenmeyer: Solving satisfiability in less than 2^n steps
            (1985) - https://doi.org/10.1016/0166-218X(85)90050-2

    Parameters:
        input_instance (Instance): The SAT instance to solve.
        with_self_sufficient_assignments_check (bool): Whether to check for and apply
            self-sufficient assignments before performing the main splitting routine.

    Returns:
        tuple[bool, int]: A tuple containing:
            - True if the instance is satisfiable, False otherwise.
            - The number of iterations (nodes explored) during the search.
    """

    # Stack holds tuples of (current_instance, current_assignments)
    stack: list[DPLLNode] = [DPLLNode(input_instance, [])]

    # For analysis purposes only
    iteration_count = 0

    while stack:
        current_node = stack.pop()
        iteration_count += 1

        # Check if no clauses left -> satisfiable
        if current_node.instance.num_clauses == 0:
            return True, iteration_count

        # Check for empty clause -> conflict
        if current_node.instance.has_empty_clause():
            # Backtrack
            continue

        # Get size of smallest occurring clause
        k = min(len(clause) for clause in current_node.instance.clauses)

        # Get first min-length clause
        clause = next(c for c in current_node.instance.clauses if len(c) == k)

        found = False
        if with_self_sufficient_assignments_check:
            for i in range(k):

                # Assume clause is: (1, -4, 8, 11, -12)
                # Create assignment turning all literals until i to False, and i to True
                # e.g. i = 3
                # {1: False, -4: False, 8: True}
                assignments = {}
                for j in range(i):
                    assignments[abs(clause[j])] = clause[j] < 0
                assignments[abs(clause[i])] = clause[i] > 0

                if is_self_sufficient_assignment(current_node.instance, assignments):
                    stack.append(
                        DPLLNode(
                            assign_and_simplify(current_node.instance, assignments),
                            current_node.assignments.copy()
                            + list(
                                var if value else -var
                                for (var, value) in assignments.items()
                            ),
                        )
                    )
                    found = True
                    break

        if found:
            # Continue with shrinked instance
            continue

        # Start: Try with i = 1, i = 2, ...
        for i in range(k - 1, -1, -1):

            # Assume clause is: (1, -4, 8, 11, -12)
            # Create assignment turning all literals until i to False, and i to True
            # e.g. i = 3
            # {1: False, -4: False, 8: True}
            assignments = {}
            for j in range(i):
                assignments[abs(clause[j])] = clause[j] < 0
            assignments[abs(clause[i])] = clause[i] > 0

            stack.append(
                DPLLNode(
                    assign_and_simplify(current_node.instance, assignments),
                    current_node.assignments.copy()
                    + list(
                        var if value else -var for (var, value) in assignments.items()
                    ),
                )
            )

    return False, iteration_count
