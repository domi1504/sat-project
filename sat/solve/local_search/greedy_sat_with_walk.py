import random
from sat.instance.instance import Instance
from sat.instance.utils import check_assignment, get_unsatisfied_clauses
from sat.solve.local_search.greedy_sat import get_variable_to_flip_gsat


def get_all_variables_of_unsatisfied_clauses(
    instance: Instance, assignment: dict[int, bool]
) -> set[int]:
    """
    Returns the set of all variables that appear in at least one unsatisfied clause
    under the current assignment.

    This is useful in probabilistic SAT algorithms where flips are restricted to
    variables directly involved in unsatisfied clauses.

    :param instance: The SAT instance.
    :param assignment: The current variable assignment.
    :return: A set of variable indices from unsatisfied clauses.
    """
    unsatisfied_clauses = get_unsatisfied_clauses(instance, assignment)
    occurring_variables = set()
    for clause in unsatisfied_clauses:
        for literal in clause:
            occurring_variables.add(abs(literal))
    return occurring_variables


def is_satisfiable_gsat_with_walk(
    instance: Instance, max_tries: int = 1000, p: float = 0.55
) -> bool:
    """
    Determines satisfiability using WalkSAT — a variant of GSAT with probabilistic walks.

    At each step:
      - With probability `p`, randomly flip a variable from an unsatisfied clause.
      - With probability `1 - p`, flip the variable that most increases satisfied clauses (GSAT strategy).

    This hybrid strategy helps avoid local optima by introducing random exploration.

    Reference:
        - Selman, Kautz, Cohen: Noise Strategies for Improving Local Search.
            (1994) - Proceedings of the Twelfth National Conference on Artificial Intelligence (Vol. 1), p. 337 - 343.

    :param instance: The SAT instance to solve.
    :param max_tries: Maximum number of random restarts (default: 1000).
    :param p: Probability of performing a random walk step (default: 0.55).
    :return: True if a satisfying assignment is found; otherwise, False.
    """

    all_variables = list(instance.get_all_variables())

    # See original paper ("multiple of #variables")
    max_flips = len(all_variables) * 2

    for _ in range(max_tries):

        # Restart: New assignment chosen u.a.r.
        assignment = {
            variable: random.choice([True, False]) for variable in all_variables
        }

        for __ in range(max_flips):

            # Check if assignments is satisfying assignment
            if check_assignment(instance, assignment):
                return True

            if random.uniform(0, 1) < p:
                # Select a variable at random from all vars occuring in an unsatisfied clause
                variables_to_choose_from = get_all_variables_of_unsatisfied_clauses(
                    instance, assignment
                )
                selected_variable = random.choice(tuple(variables_to_choose_from))
            else:
                # Use standard GSAT procedure
                selected_variable = get_variable_to_flip_gsat(instance, assignment)

            # Flip literal in assignment
            assignment[selected_variable] = not assignment[selected_variable]

    return False
