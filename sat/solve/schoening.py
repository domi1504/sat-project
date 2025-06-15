import random
from sat.instance.instance import Instance
from sat.instance.utils.utils import check_assignment, get_unsatisfied_clauses
from sat.modify.assign_and_simplify import assign_and_simplify


def is_satisfiable_schoening(instance: Instance, error_rate: float = 1e-8) -> bool:
    """

    :param instance:
    :return:
    """

    # todo. link with error rate. see schoening.
    number_iterations = int(1e4)

    all_variables = list(instance.get_all_variables())

    for _ in range(number_iterations):

        if _ % 100 == 0:
            print(_)

        # (Re)start: New assignment chosen u.a.r.
        assignment = {}
        for variable in all_variables:
            assignment[variable] = random.choice([True, False])

        for __ in range(instance.num_variables):

            # Check if assignments is satisfying assignment
            if check_assignment(instance, assignment):
                return True

            # Choose one unsatisfied clause u.a.r
            unsatisfied_clauses = get_unsatisfied_clauses(instance, assignment)
            selected_clause = unsatisfied_clauses[
                random.randint(0, len(unsatisfied_clauses) - 1)
            ]

            # Choose one variable u.a.r
            selected_variable = abs(
                selected_clause[
                    random.randint(0, len(selected_clause) - 1)
                ]
            )

            # Flip literal in assignment
            assignment[selected_variable] = not assignment[selected_variable]

    return False

