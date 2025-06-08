from typing import Callable, List
from sat.core_attributes.pure_literal import get_pure_literal
from sat.instance.instance import Instance
from sat.modify.assign_and_simplify import assign_and_simplify
from sat.solve.dpll.dpll_node import DPLLNode, CDCLNode

# todo. check, wie man das in echt in schneller implementieren würde?
#  z.b. https://github.com/jaras209/SAT_solver/blob/master/cdcl.py, "2-watched literals" (irgendne art index)

# todo. unit propagation aus den iterationen rausziehen? das praktisch eine zweite innere loop läuft, die das direkt macht
# dementsprechend gäbs nur neue CDCLNodes bei entscheidungen


def is_satisfiable_dpll_cdcl_ncbt(input_instance: Instance, heuristic: Callable[[Instance], int]) -> bool:
    """

    :param input_instance:
    :param heuristic:
    :return:
    """
    decision_level = 0
    assignments = []
    antecedent = {}
    learned_clauses = []
    trail = []  # Track order of assignments for conflict analysis

    # per clause: save original index of the clause in the list of the input_instance!
    # weitermachen.

    stack: List[CDCLNode] = [CDCLNode(input_instance, [], 0, {})]

    while stack:
        current_node = stack.pop()

        # Check if no clauses left -> satisfiable
        if current_node.instance.num_clauses == 0:
            return True

        # Check for empty clause -> conflict
        if any(len(clause) == 0 for clause in current_node.instance.clauses):

            if decision_level == 0:
                # todo. verify. necessary?
                return False

            # todo. backtrack

        # Handle unit clauses; unit propagation.
        unit_clause_found = False
        for clause in current_node.instance.clauses:
            if len(clause) == 1:
                # Unit clause found: set variable.
                current_node.antecedent[abs(unit)] = find_antecedent_clause(instance, unit)
                stack.append(
                    CDCLNode(
                        assign_and_simplify(current_node.instance, {abs(clause[0]): clause[0] > 0}),
                        current_node.assignments.copy() + [clause[0]],
                        decision_level,  # decision level only increases upon decision variables
                        {}
                    )
                )
                unit_clause_found = True
                break

        if unit_clause_found:
            # Evaluate after now removed unit clause
            continue

        # todo. pure literal

        # todo. decision.

    return False
