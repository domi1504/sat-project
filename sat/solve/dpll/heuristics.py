from random import random
from typing import Callable

from sat.instance.instance import Instance
from collections import Counter


"""
Heuristics for variable selection in DPLL SAT solvers.

This module defines a variety of variable selection heuristics used in DPLL- and CDCL-based algorithms. 
These heuristics guide which variable (literal) to branch on next in order to maximize efficiency during search.

All heuristics take in a SAT `Instance` and return a single `int` representing a literal.
The literal returned will be assigned `True` first.

Examples:
    - If the heuristic returns `3`, the solver will first try `x3 := True`, then `x3 := False`.
    - If it returns `-4`, the solver will first try `x4 := False`, then `x4 := True`.
"""


DPLLHeuristic = Callable[[Instance], int]


def dlis(instance: Instance) -> int:
    """
    Dynamic Largest Individual Sum (DLIS) heuristic.

    Selects the literal with the highest number of occurrences across all clauses.
    In case of ties, selects the literal with the smallest absolute value,
    preferring the positive literal if both polarities have the same count.

    Reference:
        - Schöning, p. 80

    :param instance: The SAT instance.
    :return: The literal to assign True first.
    """
    assert instance.num_variables > 0

    # Clauses flattened
    all_literals = [lit for clause in instance.clauses for lit in clause]

    # Count number of occurrences of each literal
    # {1: 1, 2: 3, -1: 4, ...}
    counts = Counter(all_literals)

    # Filter literals with the maximum count
    max_count = max(counts.values())
    candidates = [num for num in counts if counts[num] == max_count]

    # Choose the literal with the lowest absolute value, preferring the positive version if both are candidates
    return min(candidates, key=lambda x: (abs(x), -x))


def dlcs(instance: Instance) -> int:
    """
    Dynamic Largest Clause Sum (DLCS) heuristic.

    Selects the variable with the largest total number of occurrences of both
    positive and negative literals across all clauses.
    Returns the positive or negative literal depending on which polarity appears more frequently.

    Reference:
        - Schöning, p. 81

    :param instance: The SAT instance.
    :return: The literal to assign True first.
    """
    assert instance.num_variables > 0

    # Clauses flattened
    all_literals = [lit for clause in instance.clauses for lit in clause]

    # Count number of occurrences of each literal
    # {1: 1, 2: 3, -1: 4, ...}
    counts = Counter(all_literals)

    # Find the variable with the most occurrences (smallest in case of conflict)
    candidates = list(instance.get_all_variables())
    highest_occurrence_variable = max(candidates, key=lambda n: (counts.get(n, 0) + counts.get(-n, 0), n))

    if counts.get(highest_occurrence_variable, 0) >= counts.get(-highest_occurrence_variable, 0):
        return highest_occurrence_variable
    else:
        return -highest_occurrence_variable


def rdlcs(instance: Instance) -> int:
    """
    Random Dynamic Largest Clause Sum (RDLCS) heuristic.

    Similar to DLCS but chooses the polarity of the selected variable at random with equal probability.

    Reference:
        - SAT-Skript p. 29

    :param instance: The SAT instance.
    :return: The literal to assign True first.
    """
    assert instance.num_variables > 0

    # Clauses flattened
    all_literals = [lit for clause in instance.clauses for lit in clause]

    # Count number of occurrences of each literal
    # {1: 1, 2: 3, -1: 4, ...}
    counts = Counter(all_literals)

    # Find the variable with the most occurrences (smallest in case of conflict)
    candidates = list(instance.get_all_variables())
    highest_occurrence_variable = max(candidates, key=lambda n: (counts.get(n, 0) + counts.get(-n, 0), n))

    if random() < 0.5:
        return highest_occurrence_variable
    else:
        return -highest_occurrence_variable


def mom(instance: Instance) -> int:
    """
    Maximum Occurrence in Minimal Size Clauses (MOM) heuristic.

    Selects a variable that occurs most frequently in the smallest clauses.
    Among those, picks the variable that maximizes the product of its positive
    and negative occurrences, favoring balanced polarity distribution.
    Always returns the positive literal.

    Reference:
        - Schöning, p.81

    :param instance: The SAT instance.
    :return: The literal to assign True first.
    """

    # Get size of smallest occurring clause
    k = min(len(clause) for clause in instance.clauses)

    # k-sized clauses flattened
    all_literals_of_k_clauses = [lit for clause in instance.clauses if len(clause) == k for lit in clause]

    # Count number of occurrences of each literal
    # {1: 1, 2: 3, -1: 4, ...}
    counts_in_k_clauses = Counter(all_literals_of_k_clauses)

    # Find the variables with the most occurrences
    candidates = list(instance.get_all_variables())
    max_value = max(counts_in_k_clauses.get(n, 0) + counts_in_k_clauses.get(-n, 0) for n in candidates)

    # Find the variables with the most occurrences
    candidates = list(instance.get_all_variables())

    # Collect all numbers that achieve this max value
    candidates = list(
        n for n in candidates if counts_in_k_clauses.get(n, 0) + counts_in_k_clauses.get(-n, 0) == max_value
    )

    # Pick the candidate with the most evenly distribution between positive and negative occurrences
    # maximizing counts_in_k_clauses[+var] * counts_in_k_clauses[-var]
    # In case of conflict, take variable with smallest absolute value
    # Always return positive literal
    return max(
        candidates,
        key=lambda n: ((counts_in_k_clauses.get(n, 0) * counts_in_k_clauses.get(-n, 0)), -n)
    )


def jeroslaw_wang(instance: Instance) -> int:
    """
    Jeroslaw-Wang heuristic.

    Scores each literal by summing 2^(-clause_length) for all clauses containing it,
    selecting the literal with the highest score.
    In case of ties, picks the literal with the smallest absolute value.

    Reference:
        - Schöning, p.81

    :param instance: The SAT instance.
    :return: The literal to assign True first.
    """
    assert instance.num_variables > 0

    # Map storing scores of all literals
    scores = {}

    # Compute scores of all literals
    for clause in instance.clauses:
        for lit in clause:
            scores[lit] = scores.get(lit, 0) + 2 ** (-len(clause))

    # Get literal with best score (in case of conflict, take smallest literal)
    highscore_literal = max(scores.keys(), key=lambda n: (scores[n], -n))

    return highscore_literal


def jeroslaw_wang_two_sided(instance: Instance) -> int:
    """
    Jeroslaw-Wang Two-Sided heuristic.

    Scores variables by summing the scores of both positive and negative literals
    (each scored as in Jeroslaw-Wang).
    Selects the variable with the highest combined score and returns
    the polarity with the higher score.

    Reference:
        - Schöning, p.81
        - SAT-Skript, p. 30

    :param instance: The SAT instance.
    :return: The literal to assign True first.
    """
    assert instance.num_variables > 0

    # Map storing scores of all literals
    scores = {}

    # Compute scores of all literals
    for clause in instance.clauses:
        for lit in clause:
            scores[lit] = scores.get(lit, 0) + 2 ** (-len(clause))

    # Get variable with best score (in case of conflict, take smaller variable)
    candidates = list(instance.get_all_variables())
    highscore_variable = max(candidates, key=lambda n: (scores.get(n, 0) + scores.get(-n, 0), -n))

    if scores.get(highscore_variable, 0) >= scores.get(-highscore_variable, 0):
        return highscore_variable
    else:
        return -highscore_variable


def shortest_clause(instance: Instance) -> int:
    """
    Shortest-Clause heuristic.

    Selects the first literal from the shortest clause in the instance.

    :param instance: The SAT instance.
    :return: The literal to assign True first.
    """
    assert instance.num_variables > 0

    # Get minimal clause length
    shortest_clause_length = min(len(clause) for clause in instance.clauses)

    # Get first literal from first occurring clause with shortest length
    return next(c for c in instance.clauses if len(c) == shortest_clause_length)[0]

