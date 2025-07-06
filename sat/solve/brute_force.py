from sat.instance.instance import Instance
from sat.instance.utils import check_assignment


def is_satisfiable_brute_force(instance: Instance) -> tuple[bool, int]:
    """
    Determines whether a SAT instance is satisfiable using brute-force search.

    This function exhaustively checks all possible truth assignments to the variables
    in the instance to determine if at least one satisfies all clauses.

    :param instance: A SAT instance.
    :return: A tuple containing a boolean indicating whether a satisfying assignment exists,
             and the number of iterations performed during the search.
    """

    all_variables = instance.get_all_variables()

    # For analysis purposes only
    iteration_counter = 0

    # Iterate over all possible assignments (binary representation of assignments)
    for assignment_index in range(2**instance.num_variables):
        iteration_counter += 1

        # Convert integer to binary representation
        assignment_binary = format(assignment_index, f"0{instance.num_variables}b")

        # Parse binary number as assignment
        assignment = {
            var: val == "1" for var, val in zip(all_variables, assignment_binary)
        }

        # Check assignment
        if check_assignment(instance, assignment):
            return True, iteration_counter

    return False, iteration_counter
