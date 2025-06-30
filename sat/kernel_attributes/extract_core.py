from sat.kernel_attributes.biathlet import is_biathlet_satisfied
from sat.kernel_attributes.lovasz_local_lemma import is_lll_satisfied
from sat.kernel_attributes.one_connected_component import is_one_connected_component
from sat.kernel_attributes.renamable_horn import is_renamable_horn
from sat.kernel_attributes.toveys_crit import is_tovey_satisfied
from sat.kernel_attributes.two_sat import is_2_sat
from sat.instance.instance import Instance
from sat.kernel_attributes.utils import (
    remove_tautological_clauses,
    remove_duplicate_and_superset_clauses,
    remove_pure_literal,
    remove_unit_clause,
    merge_zwei_eige_zwillinge,
)


"""
Module for SAT instance kernelization and kernel property checks.

This module provides functions to iteratively simplify a SAT formula to its "problem kernel" by
applying various reduction rules such as removing unit clauses, tautological clauses, duplicates,
supersets, pure literals, and merging special clause pairs ("2-Eige-Zwillinge").

It also offers checks to determine whether a given SAT instance qualifies as a kernel instance,
using well-known criteria including Lovász Local Lemma, "Biathlet" property, connectivity,
Tovey's criterium, 2-SAT solvability, and the renamable Horn property.
"""


def _normalize_to_kernel_step(instance: Instance) -> tuple[Instance, bool]:
    """
    Perform a single normalization step on the SAT instance by applying
    one of the following simplifications in order:

    1. Remove unit clauses.
    2. Remove tautological clauses (clauses always true, e.g., (x1 OR !x1)).
    3. Remove duplicate and superset clauses.
    4. Remove pure literals (variables appearing with only one polarity).
    5. Merge pairs of "2-Eige-Zwillinge" clauses (clauses differing only in one literal's polarity).

    Returns immediately upon the first simplification that results in changes.

    :param instance:
        The SAT instance to normalize.

    :return:
        A tuple containing:
        - The potentially simplified instance.
        - A boolean indicating whether any change was made (True) or not (False).
    """

    # Remove unit clauses
    instance, changed = remove_unit_clause(instance)
    if changed:
        return instance, True

    # Remove ALWAYS-TRUE clauses (x1 OR !x1)
    instance, changed = remove_tautological_clauses(instance)
    if changed:
        return instance, True

    # Remove double and superset clauses
    instance, changed = remove_duplicate_and_superset_clauses(instance)
    if changed:
        return instance, True

    # Remove literals only occurring in positive or negative form
    instance, changed = remove_pure_literal(instance)
    if changed:
        return instance, True

    # Merge zwei eige zwillinge to one clause
    instance, changed = merge_zwei_eige_zwillinge(instance)
    if changed:
        return instance, True

    return instance, False


def normalize_formula_to_kernel(instance: Instance) -> Instance:
    """
    Iteratively reduce the given SAT formula to its "problem kernel" by repeatedly applying
    kernel normalization steps until no further simplifications are possible.

    The reduction applies the following transformations in each iteration:

    - Remove unit clauses (and corresponding variables).
    - Remove tautological clauses (e.g., clauses containing both a literal and its negation).
    - Remove duplicate and superset clauses.
    - Remove pure literals.
    - Merge "2-Eige-Zwillinge" clauses.

    :param instance:
        The SAT instance to normalize.

    :return:
        The reduced SAT instance representing the problem kernel.
    """

    iter_count = 0
    while True:

        instance, changed = _normalize_to_kernel_step(instance)

        if changed:
            iter_count += 1
        else:
            break

    print(f"Normalizing to problem kernel took {iter_count} iterations")
    return instance


def is_kernel_instance(instance: Instance) -> bool:
    """
    Determine whether the given SAT formula is a "problem kernel".

    This function checks if the instance is already reduced (no kernel normalization steps
    apply) and satisfies multiple kernel properties:

    - No empty clause present.
    - Lovász Local Lemma (LLL) satisfied.
    - Biathlet property satisfied.
    - Instance forms one connected component.
    - Tovey's criterium satisfied.
    - Not 2-SAT solvable.
    - Not renamable Horn.

    If all these conditions hold, the instance qualifies as a kernel instance.

    :param instance:
        The SAT instance to check.

    :return:
        True if the instance is a kernel instance, False otherwise.
    """

    _, changed = _normalize_to_kernel_step(instance)

    if changed:
        return False

    if instance.has_empty_clause():
        print("Could simplify: not kernel instance")
        return False

    if not is_lll_satisfied(instance):
        print("LLL not satisfied: is satisfiable")
        return False

    if not is_biathlet_satisfied(instance):
        print("Biathlet not satisfied: is satisfiable")
        return False

    if not is_one_connected_component(instance):
        print("not one connected component: 'splittable'")
        return False

    if not is_tovey_satisfied(instance):
        print("toveys criterium: is satisfiable")
        return False

    if is_2_sat(instance):
        print("2-SAT: polynomially solvable")
        return False

    if is_renamable_horn(instance):
        print("Renamable Horn: polynomially solvable")
        return False

    return True
