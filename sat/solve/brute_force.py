from sat.instance.instance import Instance
from sat.instance.utils import check_assignment


def is_satisfiable_brute_force(instance: Instance) -> bool:
    """
    Determines whether a SAT instance is satisfiable using brute-force search.

    This function exhaustively checks all possible truth assignments to the variables
    in the instance to determine if at least one satisfies all clauses.

    :param instance: A SAT instance.
    :return: True if a satisfying assignment exists, False otherwise.
    """

    all_variables = instance.get_all_variables()

    # Iterate over all possible assignments (binary representation of assignments)
    for assignment_index in range(2 ** instance.num_variables):

        # Convert integer to binary representation
        assignment_binary = format(assignment_index, f'0{instance.num_variables}b')

        # Parse binary number as assignment
        assignment = {var: val == '1' for var, val in zip(all_variables, assignment_binary)}

        # Check assignment
        if check_assignment(instance, assignment):
            return True

    return False

