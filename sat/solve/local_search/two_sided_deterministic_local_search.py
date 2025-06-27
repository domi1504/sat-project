import math
from sat.instance.instance import Instance
from sat.solve.local_search.search_hamming_ball import search_hamming_ball


def is_satisfiable_two_sided_deterministic_local_search(instance: Instance) -> bool:
    """
    Determines satisfiability using a two-sided deterministic local search strategy.

    This method is primarily suited for 3-SAT instances.
        (Because runtime complexity not better than brute-force for k >= 4)
    It performs local search from two starting points: the all-False (0...0) and all-True (1...1)
    assignments. For each starting point, it searches the Hamming ball of radius n/2
    (where n is the number of variables) for a satisfying assignment.

    Reference:
        - Schöning, p.94 f.

    :param instance: A SAT instance containing clauses and variables.
    :return: True if a satisfying assignment is found within either Hamming ball, False otherwise.
    """

    all_0_assignment = {variable: False for variable in instance.get_all_variables()}
    all_1_assignment = {variable: True for variable in instance.get_all_variables()}

    if search_hamming_ball(instance, all_0_assignment, int(math.ceil(instance.num_variables / 2))):
        return True

    if search_hamming_ball(instance, all_1_assignment, int(math.ceil(instance.num_variables / 2))):
        return True

    return False

