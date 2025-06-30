from sat.instance.assign_and_simplify import assign_and_simplify
from sat.instance.instance import Instance


def remove_unit_clause(instance: Instance) -> tuple[Instance, bool]:
    """
    Detect and remove next unit clause from the given SAT instance by assigning the literal.

    If a unit clause (a clause with exactly one literal) is found, the function applies the
    corresponding assignment to simplify the instance and returns the simplified instance
    along with a flag indicating a unit claus was removed.

    :param instance:
        The SAT instance to simplify.

    :return:
        A tuple containing:
        - The simplified SAT instance after applying the unit clause assignment (if any).
        - A boolean flag that is True if a unit clause was found and processed, False otherwise.
    """

    for clause in instance.clauses:
        if len(clause) == 1:
            return assign_and_simplify(instance, {clause[0]: clause[0] > 0}), True

    return instance, False


def remove_tautological_clauses(instance: Instance) -> tuple[Instance, bool]:

    def is_clause_not_tautological(clause: tuple[int, ...]) -> bool:
        for lit in clause:
            if -lit in clause:
                # Clause is tautology
                return False
        return True

    filtered_clauses = list(filter(is_clause_not_tautological, instance.clauses))

    if len(filtered_clauses) == instance.num_clauses:
        return instance, False

    return Instance(filtered_clauses), True


def remove_pure_literal(instance: Instance) -> tuple[Instance, bool]:
    """
    Detect and remove pure literal from the given SAT instance.

    A pure literal is a variable that appears in only one polarity
    (either always positive or always negative) throughout all clauses.
    Removing a pure literal by assigning it accordingly simplifies the instance.

    The function finds the first pure literal and performs the assignment and simplification.

    :param instance:
        The SAT instance containing clauses as tuples of literals.

    :return:
        A tuple containing:
        - The simplified Instance after assigning the pure literal (if found), or the original instance.
        - A boolean indicating whether a pure literal was found and removed (True), or not (False).
    """

    all_variables = instance.get_all_variables()

    for variable in all_variables:
        if all(variable not in clause for clause in instance.clauses):
            # Variable only appears in negative form
            return assign_and_simplify(instance, {variable: False}), True
        if all(-variable not in clause for clause in instance.clauses):
            # Variable only appears in positive form
            return assign_and_simplify(instance, {variable: True}), True

    # No pure literals found
    return instance, False


def remove_duplicate_and_superset_clauses(instance: Instance) -> tuple[Instance, bool]:
    """
    Remove duplicate and superset clauses from the given SAT instance.

    Duplicate clauses are those with exactly the same literals.
    Superset clauses are clauses that fully contain all literals of another smaller clause,
    making them redundant since the smaller clause subsumes them.

    :param instance:
        The SAT instance containing clauses as tuples of literals.

    :return:
        A tuple containing:
        - A new Instance with duplicates and superset clauses removed.
        - A boolean indicating whether any clauses were removed (True) or not (False).
    """

    def are_clauses_identical(clause1, clause2):
        return len(clause1) == len(clause2) and all(lit in clause2 for lit in clause1)

    def is_subset_clause(small, big):
        return all(lit in big for lit in small)

    # Remove duplicates first
    unique_clauses: list[tuple[int, ...]] = []
    for clause in instance.clauses:
        if not any(are_clauses_identical(clause, c) for c in unique_clauses):
            unique_clauses.append(clause)

    # Remove superset clauses
    final_clauses = []
    for clause in unique_clauses:
        if not any(
            is_subset_clause(other, clause) and len(other) < len(clause)
            for other in unique_clauses
        ):
            final_clauses.append(clause)

    if len(final_clauses) == instance.num_clauses:
        return instance, False

    return Instance(final_clauses), True


def merge_zwei_eige_zwillinge(instance: Instance) -> tuple[Instance, bool]:
    """
    Identify and merge pairs of clauses in the SAT instance that differ
    in exactly one variable's polarity, simplifying the instance.

    Specifically:
        - Two clauses are selected if they differ only on one variable,
          where one clause contains the positive literal and the other the negative literal.
        - The function removes the differing literal from the first clause,
          and removes the second clause entirely.

    :param instance:
        The SAT instance represented internally by its bit matrix.

    :return:
        A tuple containing:
        - The simplified instance with merged clauses (or original if no merge was possible).
        - A boolean indicating whether any merge was performed (True) or not (False).
    """

    for i in range(instance.num_clauses - 1):
        for j in range(i + 1, instance.num_clauses):

            c1 = set(instance.clauses[i])
            c2 = set(instance.clauses[j])

            # Get union of all values that are in only one of the two clauses
            diff = c1.symmetric_difference(c2)

            # Check if they differ in exactly two literals, which must be negations of each other
            if len(diff) == 2:
                lit1, lit2 = diff
                if lit1 == -lit2:
                    # They differ only by one variable's polarity
                    # Create new clause by removing that literal from the first clause
                    new_clause = c1 - {lit1}

                    # Build new list of clauses:
                    # - Replace clause i with new_clause
                    # - Remove clause j
                    new_clauses = []
                    for k, c in enumerate(instance.clauses):
                        if k == i:
                            # Insert the new merged clause (as a tuple sorted for consistency)
                            new_clauses.append(tuple(sorted(new_clause)))
                        elif k == j:
                            # Skip clause j (remove)
                            continue
                        else:
                            new_clauses.append(c)

                    return Instance(new_clauses), True

    return instance, False
