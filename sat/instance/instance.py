import numpy as np

from sat.instance.bit_matrix.bit_matrix import bit_matrix_valid, clauses_to_bit_matrix
from sat.instance.clauses.clauses import bit_matrix_to_clauses, clauses_valid, are_clauses_empty, count_number_variables


class Instance:

    def __init__(self, clauses: set[tuple[int, ...]]):
        self.clauses: set[tuple[int, ...]] = clauses
        assert clauses_valid(self.clauses)

        # Compute bit matrix if possible
        if len(self.clauses) > 0 and not are_clauses_empty(self.clauses):
            self.bit_matrix: np.ndarray = clauses_to_bit_matrix(self.clauses)
            assert bit_matrix_valid(self.bit_matrix)

        self.num_clauses = len(self.clauses)
        self.num_variables = count_number_variables(self.clauses)

    def __str__(self):
        return f"Instance with {self.num_variables} variables and {self.num_clauses} clauses"

    def get_all_variables(self) -> set[int]:
        all_variables = set()
        for clause in self.clauses:
            for lit in clause:
                all_variables.add(abs(lit))
        return all_variables


def normalize_clauses(clauses: set[tuple[int, ...]]) -> set[tuple[int, ...]]:

    # Normalize clauses: 1-based, vars from exactly [1, ..., n]
    normalized_clauses = set()

    # Count variables & create mapping to indices
    var_name_map = {}
    cur_var_name = 1
    for clause in clauses:
        for lit in clause:
            var = abs(lit)
            if var not in var_name_map.keys():
                var_name_map[var] = cur_var_name
                cur_var_name += 1

    # Fill normalized clauses
    for clause in clauses:
        renamed_clause = tuple((1 if lit > 0 else -1) * var_name_map[abs(lit)] for lit in clause)
        normalized_clauses.add(renamed_clause)

    return normalized_clauses


def get_instance_from_bit_matrix(matrix: np.ndarray) -> Instance:
    clauses = bit_matrix_to_clauses(matrix)
    return Instance(clauses)

