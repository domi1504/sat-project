import copy
import numpy as np
from sat.core_attributes.lovasz_local_lemma import is_lll_satisfied
from sat.core_attributes.one_connected_component import is_one_connected_component
from sat.core_attributes.renamable_horn import is_renamable_horn
from sat.core_attributes.toveys_crit import is_tovey_satisfied
from sat.core_attributes.two_sat import is_2_sat
from sat.instance.instance import Instance, get_instance_from_bit_matrix


def _remove_clauses_and_literals(matrix: np.ndarray, clauses: set, literals: set) -> np.ndarray:

    clauses = sorted(clauses)
    literals = sorted(literals)

    for index in clauses[::-1]:
        matrix = np.delete(matrix, index, axis=0)
    for column in literals[::-1]:
        matrix = np.delete(matrix, column, axis=1)

    return matrix


def _remove_empty_clauses(matrix: np.ndarray) -> tuple[np.ndarray, bool]:
    to_remove_clauses = set()
    for i in range(matrix.shape[0]):
        if not np.any(matrix[i] == 1):
            to_remove_clauses.add(i)

    if len(to_remove_clauses) > 0:
        matrix = _remove_clauses_and_literals(matrix, to_remove_clauses, set())
        return matrix, True
    return matrix, False


def _remove_unit_clauses(matrix: np.ndarray) -> tuple[np.ndarray, bool]:
    to_remove_clauses = set()
    to_remove_literals = set()
    for i in range(matrix.shape[0]):
        if np.sum(matrix[i]) == 1:
            # Unit clause identified
            # 1. Find variable
            lit_index = np.where(matrix[i] == 1)[0][0]
            lit_index_2 = (lit_index - 1) if lit_index % 2 == 1 else lit_index + 1

            # 2. Remove all clauses containing this variable (positive or negative)
            for j in range(matrix.shape[0]):
                if matrix[j, lit_index] == 1 or matrix[j, lit_index_2] == 1:
                    to_remove_clauses.add(j)
            # 3. Remove this variable
            to_remove_literals.add(lit_index)
            to_remove_literals.add(lit_index_2)

    if len(to_remove_clauses) > 0 or len(to_remove_literals) > 0:
        matrix = _remove_clauses_and_literals(matrix, to_remove_clauses, to_remove_literals)
        return matrix, True
    return matrix, False


def _remove_always_true_clauses(matrix: np.ndarray) -> tuple[np.ndarray, bool]:
    to_remove_clauses = set()
    for i in range(matrix.shape[0]):
        for j in range(0, matrix.shape[1], 2):
            if matrix[i, j] == 1 and matrix[i, j+1] == 1:
                to_remove_clauses.add(i)

    if len(to_remove_clauses) > 0:
        matrix = _remove_clauses_and_literals(matrix, to_remove_clauses, set())
        return matrix, True
    return matrix, False


def _remove_double_and_superset_clauses(matrix: np.ndarray) -> tuple[np.ndarray, bool]:
    to_remove_clauses = set()
    for i in range(matrix.shape[0]):
        # Check if clause i is superset of any other clause
        for j in range(matrix.shape[0]):
            if i == j:
                continue
            is_i_superset_of_j = True
            for k in range(matrix.shape[1]):
                if matrix[j, k] == 1 and matrix[i, k] == 0:
                    is_i_superset_of_j = False
            if is_i_superset_of_j:
                to_remove_clauses.add(i)

    if len(to_remove_clauses) > 0:
        matrix = _remove_clauses_and_literals(matrix, to_remove_clauses, set())
        return matrix, True
    return matrix, False


def _remove_pure_literals(matrix: np.ndarray) -> tuple[np.ndarray, bool]:
    to_remove_clauses = set()
    to_remove_literals = set()
    for j in range(0, matrix.shape[1], 2):
        if (not np.any(matrix[:, j])) or (not np.any(matrix[:, j + 1])):
            # 2. Remove all clauses containing this variable (positive or negative)
            for k in range(matrix.shape[0]):
                if matrix[k, j] == 1 or matrix[k, j + 1] == 1:
                    to_remove_clauses.add(k)
            # 3. Remove this variable
            to_remove_literals.add(j)
            to_remove_literals.add(j + 1)

    if len(to_remove_clauses) > 0 or len(to_remove_literals) > 0:
        matrix = _remove_clauses_and_literals(matrix, to_remove_clauses, to_remove_literals)
        return matrix, True

    return matrix, False


def _merge_zwei_eige_zwillinge(matrix: np.ndarray) -> tuple[np.ndarray, bool]:

    affected_clauses = []
    affected_variable = -1

    for i in range(matrix.shape[0] - 1):
        for j in range(i + 1, matrix.shape[0]):

            c1 = matrix[i]
            c2 = matrix[j]

            is_hit = True
            difference_at_index = -1
            for index in range(0, matrix.shape[1], 2):

                # Both same
                if c1[index] == c2[index] and c1[index + 1] == c2[index + 1]:
                    continue

                # One 00, other not
                if (c1[index] == 0 and c1[index + 1] == 0) or (c2[index] == 0 and c2[index + 1] == 0):
                    is_hit = False
                    break

                # 01 and 10
                if difference_at_index == -1:
                    difference_at_index = index
                else:
                    is_hit = False
                    break

            if is_hit:
                affected_clauses = (i, j)
                affected_variable = difference_at_index
                break

        if len(affected_clauses) > 0:
            break

    if len(affected_clauses) > 0:

        # In first clause: remove affected literal
        matrix[affected_clauses[0], affected_variable] = 0
        matrix[affected_clauses[0], affected_variable + 1] = 0

        # In second close: remove whole clause
        matrix = _remove_clauses_and_literals(matrix, {affected_clauses[1]}, set())

        return matrix, True

    return matrix, False


def _normalize_to_core_step(matrix: np.ndarray) -> tuple[np.ndarray, bool]:
    """

    :param matrix:
    :return: Did changes occur?
    """

    # Remove empty clauses
    matrix, changed = _remove_empty_clauses(matrix)
    if changed:
        return matrix, True

    # Remove unit clauses
    matrix, changed = _remove_unit_clauses(matrix)
    if changed:
        return matrix, True

    # Remove ALWAYS-TRUE clauses (x1 OR !x1)
    matrix, changed = _remove_always_true_clauses(matrix)
    if changed:
        return matrix, True

    # Remove double and superset clauses
    matrix, changed = _remove_double_and_superset_clauses(matrix)
    if changed:
        return matrix, True

    # Remove literals only occurring in positive or negative form
    matrix, changed = _remove_pure_literals(matrix)
    if changed:
        return matrix, True

    # Merge zwei eige zwillinge to one clause
    matrix, changed = _merge_zwei_eige_zwillinge(matrix)
    if changed:
        return matrix, True

    return matrix, False


def normalize_formula_to_core(instance: Instance) -> Instance:
    """
    Reduce to the "problem core"

    - [0] Remove empty clauses
    - [0] Remove unit clauses (and variables)
    - [1] Remove always-true clauses (x1 or !x1)
    - [2] Remove double and superset clauses
    - [3] Remove variables only occurring in positive / negative form
    - [4] Merge "2-Eige-Zwillinge"

    """

    iter_count = 0
    while True:

        updated_bit_matrix, changed = _normalize_to_core_step(instance.get_bit_matrix())

        if changed:
            iter_count += 1
        else:
            break

    print(f"Normalizing to problem core took {iter_count} iterations")
    return get_instance_from_bit_matrix(updated_bit_matrix)


def is_formula_core(instance: Instance) -> bool:
    """
    Check whether given formula is a "problem core".

    Call normalize-to-core on a copy and check if changes occurred.

    :param instance:
    :return:
    """
    matrix_copy = copy.deepcopy(instance.get_bit_matrix())
    _, changed = _normalize_to_core_step(matrix_copy)

    if changed:
        return False

    if not is_lll_satisfied(instance):
        raise Exception("LLL not satisfied: trivially satisfiable")

    if not is_one_connected_component(instance):
        raise Exception("not one connected component: trivially 'splittable'")

    if not is_tovey_satisfied(instance):
        raise Exception("toveys criterium: trivially satisfiable")

    if is_2_sat(instance):
        raise Exception("2-SAT: trivially solvable")

    if is_renamable_horn(instance):
        raise Exception("Renamable Horn: trivially solvable")

    return True
