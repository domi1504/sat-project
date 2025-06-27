from sat.instance.instance import Instance
from sat.solve.local_search.cover_code import generate_cover_code
from sat.solve.local_search.search_hamming_ball import search_hamming_ball


def is_satisfiable_dantsin_local_search(instance: Instance) -> bool:
    """
    Determines the satisfiability of a SAT instance using the Dantsin et al. local search algorithm.

    This method systematically explores the search space by evaluating a covering code —
    a set of representative assignments — and performs a bounded-radius local search
    (within a Hamming ball) around each codeword.

    References:
        - Schöning, p.99 f.
        - Dantsin et al.: A deterministic (2−2/(k+1))^n algorithm for k-SAT based on local search.
            (2002) - https://doi.org/10.1016/S0304-3975(01)00174-8

    :param instance: The SAT instance to be solved.
    :return: True if a satisfying assignment is found, False otherwise.
    """

    delta = 0.25
    cover_code = generate_cover_code(instance.num_variables, delta)

    for assignment in cover_code:

        # Search through hamming ball with radius delta * n
        if search_hamming_ball(instance, assignment, int(instance.num_variables * delta)):
            return True

    return False

