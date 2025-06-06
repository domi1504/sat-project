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
                if ass in clause or -ass in clause:
                    print("a")
                # assert ass not in clause and -ass not in clause
