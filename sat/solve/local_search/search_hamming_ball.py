import random
from sat.instance.instance import Instance
from sat.instance.utils import check_assignment, get_unsatisfied_clauses


def search_hamming_ball(instance: Instance, assignment: dict[int, bool], radius: int) -> bool:
    """
    Performs a recursive local search in the Hamming ball of specified radius of a given assignment.

    This function checks whether a satisfying assignment exists within a given
    Hamming distance (`radius`) from the current assignment. It selects an unsatisfied
    clause at random and tries flipping each literal in the clause, recursively
    exploring the reduced search space.

    Reference:
        - Schöning p.94 f.

    :param instance: A SAT instance to evaluate.
    :param assignment: A mapping from variable indices to boolean values representing the current assignment.
    :param radius: The maximum Hamming distance allowed for exploring alternative assignments.
    :return: True if a satisfying assignment is found within the Hamming ball, False otherwise.
    """
    assert len(assignment) == instance.num_variables

    if check_assignment(instance, assignment):
        # Found satisfying assignment
        return True

    if radius == 0:
        # Search space exhausted
        return False

    # Pick one unsatisfied clause randomly
    unsatisfied_clauses = get_unsatisfied_clauses(instance, assignment)
    selected_clause = unsatisfied_clauses[
        random.randint(0, len(unsatisfied_clauses) - 1)
    ]

    # Try to flip every contained literal, search recursively with decreased radius
    for literal in selected_clause:
        if search_hamming_ball(
            instance,
            {**assignment, abs(literal): not assignment[abs(literal)]},
            radius - 1
        ):
            return True

    return False



