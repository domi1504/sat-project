import math
from sat.instance.instance import Instance
from sat.solve.local_search.search_hamming_ball import search_hamming_ball


def is_satisfiable_two_sided_deterministic_local_search(instance: Instance) -> bool:
    """
    Only somewhat sensible for 3-SAT.
    Apply local search. Use 0...0 and 1...1 as initial assignments
    and for both search through the hamming balls with radius n/2.

    :param instance:
    :return:
    """

    all_0_assignment = {variable: False for variable in instance.get_all_variables()}
    all_1_assignment = {variable: True for variable in instance.get_all_variables()}

    if search_hamming_ball(instance, all_0_assignment, int(math.ceil(instance.num_variables / 2))):
        return True

    if search_hamming_ball(instance, all_1_assignment, int(math.ceil(instance.num_variables / 2))):
        return True

    return False

