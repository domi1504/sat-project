from typing import Callable, List
from sat.core_attributes.pure_literal import get_pure_literal
from sat.instance.instance import Instance
from sat.modify.assign_and_simplify import assign_and_simplify_cdcl
from sat.solve.dpll.dpll_node import CDCLNode

"""
Gute quelle: https://users.aalto.fi/%7Etjunttil/2020-DP-AUT/notes-sat/cdcl.html 
Trail <=> assignments + antecedents
"""

# todo(sometime). unit propagation etc. aus den iterationen rausziehen?
#  das praktisch eine zweite innere loop läuft, die das direkt macht

# todo(sometime). auch sowas wie conflict handling rausziehen?


def is_satisfiable_dpll_cdcl_ncbt(input_instance: Instance, heuristic: Callable[[Instance], int]) -> bool:
    """

    :param input_instance:
    :param heuristic:
    :return:
    """

    decision_level = 0

    # Here, learned clauses will be added. All clauses have a distinct index. When new ones are added,
    # they get appended at the end. No old indices get modified.
    all_clauses = input_instance.clauses.copy()

    stack: List[CDCLNode] = [
        CDCLNode(
            input_instance,
            [],  # no assignments at start.
            {},  # no corresponding decision levels.
            {},  # no corresponding antecedents.
            list(range(input_instance.num_clauses)),  # every clause at original index in the beginning.
        )
    ]

    # DPLL search procedure
    while stack:
        current_node = stack.pop()

        """ Check if no clauses left -> satisfiable """
        if current_node.instance.num_clauses == 0:
            return True

        """ Check for empty clause -> conflict """
        if current_node.instance.has_empty_clause():

            if decision_level == 0:
                # no backtrack possible.
                return False

            """ Conflict analysis """

            """ Step 1: Find First UIP """

            # Get conflict clause (now empty clause under current assignment)
            empty_clause_index = current_node.instance.clauses.index(())
            conflict_clause = all_clauses[current_node.indices_in_original[empty_clause_index]]

            assignments_copy = current_node.assignments.copy()
            # See https://stackoverflow.com/questions/67379492/finding-the-first-uip-in-an-inference-graph
            first_uip_cut = set()

            # Start with conflict clause
            for lit in conflict_clause:
                first_uip_cut.add(-lit)

            # Keep going until only one literal of latest decision level remains
            while len([1 for e in first_uip_cut if current_node.decision_levels[abs(e)] == decision_level]) > 1:
                next_lit = assignments_copy.pop()
                if next_lit in first_uip_cut:
                    # Remove from set
                    first_uip_cut.remove(next_lit)
                    # Add its predecessors of the implication graph
                    antecedent_clause_index = current_node.antecedent[abs(next_lit)]
                    assert antecedent_clause_index is not None  # immer?
                    antecedent_clause = all_clauses[antecedent_clause_index]
                    for ant_clause_lit in antecedent_clause:
                        if ant_clause_lit != next_lit:
                            first_uip_cut.add(-ant_clause_lit)  # sic. negated form.

            # This would be the First UIP (actually not necessary anymore)
            # first_uip = next(e for e in first_uip_cut if current_node.decision_levels[abs(e)] == decision_level)

            """ Step 2: Get cut from First UIP & add learned clause """

            # Learned clause: negation of every literal that has an edge over the cut (collected exactly in first_uip_cut)
            learned_clause = tuple(-lit for lit in list(first_uip_cut))

            # Add learned clause to all clauses
            all_clauses.append(learned_clause)

            # Add learned clause to all instances in stack
            for node in stack:
                # If already satisfied by the node's assignment: skip.
                if any(lit in node.assignments for lit in learned_clause):
                    continue
                # Leave out already falsified literals in the node's assignment
                new_clause = tuple(lit for lit in learned_clause if -lit not in node.assignments)
                node.instance = Instance(node.instance.clauses[:] + [new_clause])
                node.indices_in_original = node.indices_in_original + [len(all_clauses) - 1]

            """ Step 3: Non-chronological backtrack  """

            if len(learned_clause) == 1:
                # Go to beginning
                backtrack_level = 0
            else:
                # Get second highest decision level appearing in learned clause
                learned_clause_decision_levels = tuple(
                    map(
                        lambda lit: current_node.decision_levels[abs(lit)],
                        learned_clause,
                    )
                )
                backtrack_level = sorted(learned_clause_decision_levels)[-2]

            # Remove all calls from stack that are above that decision level
            stack = list([
                node for node in stack if all(level <= backtrack_level for level in node.decision_levels.values())
            ])
            
            # Replace current node with backtracked version
            backtracked_assignments = current_node.assignments.copy()
            backtracked_decision_levels = {**current_node.decision_levels}
            backtracked_antecedents = {**current_node.antecedent}
            while len(backtracked_assignments) > 0 and backtracked_decision_levels[abs(backtracked_assignments[-1])] > backtrack_level:
                var = abs(backtracked_assignments.pop())
                del backtracked_decision_levels[var]
                del backtracked_antecedents[var]
            # Retrieve backtracked instance & pointers
            backtracked_instance = Instance(all_clauses)
            backtracked_pointers = list(range(len(all_clauses)))
            for lit in backtracked_assignments:
                backtracked_instance, backtracked_pointers = assign_and_simplify_cdcl(
                    backtracked_instance,
                    {abs(lit): lit > 0},
                    backtracked_pointers,
                )
            stack.append(
                CDCLNode(
                    backtracked_instance,
                    backtracked_assignments,
                    backtracked_decision_levels,
                    backtracked_antecedents,
                    backtracked_pointers,
                )
            )

            # Set decision level
            decision_level = backtrack_level

            # Next iteration
            continue

        """ Handle unit clauses; unit propagation """
        unit_clause_found = False
        for index, clause in enumerate(current_node.instance.clauses):
            if len(clause) == 1:
                # Unit clause found: set variable.
                updated_instance, updated_pointers = assign_and_simplify_cdcl(
                    current_node.instance,
                    {abs(clause[0]): clause[0] > 0},
                    current_node.indices_in_original,
                )
                stack.append(
                    CDCLNode(
                        updated_instance,
                        current_node.assignments.copy() + [clause[0]],
                        {**current_node.decision_levels, abs(clause[0]): decision_level},  # decision level only increases upon decision variables
                        {**current_node.antecedent, abs(clause[0]): current_node.indices_in_original[index]},
                        updated_pointers,
                    )
                )
                unit_clause_found = True
                break
        if unit_clause_found:
            # Evaluate after now removed unit clause
            continue

        """ Check for pure literals """
        pure_literal = get_pure_literal(current_node.instance)
        if pure_literal is not None:
            # Pure literal found: set variable.
            updated_instance, updated_pointers = assign_and_simplify_cdcl(
                current_node.instance,
                {abs(pure_literal): pure_literal > 0},
                current_node.indices_in_original,
            )
            stack.append(
                CDCLNode(
                    updated_instance,
                    current_node.assignments.copy() + [pure_literal],
                    {**current_node.decision_levels, abs(pure_literal): decision_level},  # decision level only increases upon decision variables
                    {**current_node.antecedent, abs(pure_literal): None},  # in case of pure literals: no antecedent.
                    updated_pointers,
                )
            )
            # Evaluate after now removed pure literal
            continue

        """ New decision """
        decision_level += 1
        # Use heuristic to select next literal
        # If "3" is returned: will first try to set 3 := True, then False.
        # If "-4" is returned: will first try to set 4 := False, then True.
        literal = heuristic(current_node.instance)

        # Try both branches with non-chronological tracking
        for value in [-literal, literal]:
            new_instance, new_indices = assign_and_simplify_cdcl(
                current_node.instance,
                {abs(literal): value > 0},
                current_node.indices_in_original
            )
            stack.append(
                CDCLNode(
                    new_instance,
                    current_node.assignments.copy() + [value],
                    {**current_node.decision_levels, abs(literal): decision_level},  # now increased decision level
                    {**current_node.antecedent, abs(literal): None},  # decision literal has no antecedent
                    new_indices,
                )
            )

    return False
