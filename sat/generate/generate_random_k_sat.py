from sat.instance.instance import Instance
import random


def generate_random_k_sat_instance(n: int, m: int, k: int) -> Instance:
    """
    Generate a random k-SAT instance in CNF form.

    :param n: Number of boolean variables to choose from.
    :param m: Number of clauses to generate.
    :param k: Literals per clause (k-SAT specification).
    :return: Instance object containing generated clauses.
    """
    assert k <= n, "k cannot be greater than n"

    # Create variable pool (1 to n)
    all_variables = list(range(1, n + 1))

    # Initialize clause container
    clauses: list[tuple[int, ...]] = []

    # Generate m clauses
    for _ in range(m):
        # Randomly select k distinct variables
        clause_variables = random.sample(all_variables, k)

        # Randomly negate variables (50% probability)
        clause = tuple(
            variable if random.uniform(0, 1) < 0.5 else -variable
            for variable in clause_variables
        )
        clauses.append(clause)

    return Instance(clauses)
