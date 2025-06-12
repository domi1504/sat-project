from typing import List
from sat.instance.instance import Instance


class DPLLNode:
    def __init__(self, instance: Instance, assignments: List[int]):

        # This is the remaining instance at the current DPLL call
        self.instance = instance

        # These are the assignments already made leading up to this call
        # [1, -4, 2] <=> x1 => True, x4 => False, x2 => True
        self.assignments = assignments

        # Note: Literals of these variables will not be contained in the instance anymore (simplified)
        for clause in self.instance.clauses:
            for ass in self.assignments:
                assert ass not in clause and -ass not in clause


class CDCLNode(DPLLNode):

    # A DPLLNode with additional attributes
    def __init__(
        self,
        instance: Instance,
        assignments: List[int],
        decision_levels: dict,
        antecedent: dict,
        indices_in_original: list[int],
    ):
        super().__init__(instance, assignments)

        # For each clause in instance.clauses:
        #   what is the index of the corresponding original clause in the original input instance
        self.indices_in_original: list[int] = indices_in_original

        # For every variable in the assignment, what is its decision level (= number of set decision variables up & incl. to this point)
        self.decision_levels: dict = decision_levels

        # For every variable in the assignment, what was the clause implying its value (in unit prop)?
        # The values of this dict are ints, the index of the clause in "global" all_clauses list.
        self.antecedent: dict = antecedent

    def get_max_decision_level(self):
        return max(self.decision_levels.values())
