from random import random
from sat.instance.instance import Instance
from collections import Counter


"""
All heuristics take in an instance and return the literal which will be assigned to True first.
If "3" is returned: will first try to set 3 := True, then False.
If "-4" is returned: will first try to set 4 := False, then True.
"""


def dlis(instance: Instance) -> int:
    """
    Dynamic Largest Individual Sum.


    :param instance:
    :return:
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
    Dynamic Largest Clause Sum.

    :param instance:
    :return:
    """
    assert instance.num_variables > 0

    # Clauses flattened
    all_literals = [lit for clause in instance.clauses for lit in clause]

    # Count number of occurrences of each literal
    # {1: 1, 2: 3, -1: 4, ...}
    counts = Counter(all_literals)

    # Find the variable with the most occurrences (smallest in case of conflict)
    candidates = list(range(1, instance.num_variables + 1))
    highest_occurrence_variable = max(candidates, key=lambda n: (counts.get(n, 0) + counts.get(-n, 0), n))

    if counts.get(highest_occurrence_variable, 0) >= counts.get(-highest_occurrence_variable, 0):
        return highest_occurrence_variable
    else:
        return -highest_occurrence_variable


def rdlcs(instance: Instance) -> int:
    """
    Random Dynamic Largest Clause Sum.

    :param instance:
    :return:
    """
    assert instance.num_variables > 0

    # Clauses flattened
    all_literals = [lit for clause in instance.clauses for lit in clause]

    # Count number of occurrences of each literal
    # {1: 1, 2: 3, -1: 4, ...}
    counts = Counter(all_literals)

    # Find the variable with the most occurrences (smallest in case of conflict)
    candidates = list(range(1, instance.num_variables + 1))
    highest_occurrence_variable = max(candidates, key=lambda n: (counts.get(n, 0) + counts.get(-n, 0), n))

    if random() < 0.5:
        return highest_occurrence_variable
    else:
        return -highest_occurrence_variable


def mom(instance: Instance) -> int:
    """
    Maximum Occurrence in Minimal Size Clauses

    :param instance:
    :return:
    """

    # Get size of smallest occurring clause
    k = min(len(clause) for clause in instance.clauses)

    # k-sized clauses flattened
    all_literals_of_k_clauses = [lit for clause in instance.clauses if len(clause) == k for lit in clause]

    # Count number of occurrences of each literal
    # {1: 1, 2: 3, -1: 4, ...}
    counts_in_k_clauses = Counter(all_literals_of_k_clauses)

    # Find the variables with the most occurrences
    candidates = list(range(1, instance.num_variables + 1))
    max_value = max(counts_in_k_clauses.get(n, 0) + counts_in_k_clauses.get(-n, 0) for n in candidates)

    # Find the variables with the most occurrences
    candidates = list(range(1, instance.num_variables + 1))

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


def boehm(instance: Instance) -> int:
    raise NotImplemented()


def jeroslaw_wang(instance: Instance) -> int:
    """
    Jeroslaw-Wang.

    :param instance:
    :return:
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
    Jeroslaw-Wang, Two-Sided.

    :param instance:
    :return:
    """
    assert instance.num_variables > 0

    # Map storing scores of all literals
    scores = {}

    # Compute scores of all literals
    for clause in instance.clauses:
        for lit in clause:
            scores[lit] = scores.get(lit, 0) + 2 ** (-len(clause))

    # Get variable with best score (in case of conflict, take smaller variable)
    candidates = list(range(1, instance.num_variables + 1))
    highscore_variable = max(candidates, key=lambda n: (scores.get(n, 0) + scores.get(-n, 0), -n))

    if scores.get(highscore_variable, 0) >= scores.get(-highscore_variable, 0):
        return highscore_variable
    else:
        return -highscore_variable


def shortest_clause(instance: Instance) -> int:
    """
    Shortest-Clause (basis for Monien-Speckenmeyer)

    :param instance:
    :return:
    """
    assert instance.num_variables > 0

    # Get minimal clause length
    shortest_clause_length = min(len(clause) for clause in instance.clauses)

    # Get first literal from first occurring clause with shortest length
    return next(c for c in instance.clauses if len(c) == shortest_clause_length)[0]

