from typing import Optional

import numpy as np

from sat.instance.bit_matrix.bit_matrix import bit_matrix_valid, clauses_to_bit_matrix
from sat.instance.clauses.clauses import bit_matrix_to_clauses, clauses_valid, are_clauses_empty


class Instance:

    def __init__(self, clauses: list[tuple[int, ...]]):
        self.clauses: list[tuple[int, ...]] = clauses
        assert clauses_valid(self.clauses)
        self.num_clauses: int = len(self.clauses)
        self.num_variables: int = len(self.get_all_variables())
        self.bit_matrix: Optional[np.ndarray] = None

    def __str__(self):
        return f"Instance with {self.num_variables} variables and {self.num_clauses} clauses"

    def get_bit_matrix(self) -> np.ndarray:
        if self.bit_matrix is not None:
            return self.bit_matrix
        if len(self.clauses) > 0 and not are_clauses_empty(self.clauses):
            self.bit_matrix = clauses_to_bit_matrix(self.clauses)
            assert bit_matrix_valid(self.bit_matrix)
            return self.bit_matrix
        else:
            raise Exception("Bit matrix not computable")

    def get_all_variables(self) -> set[int]:
        all_variables = set()
        for clause in self.clauses:
            for lit in clause:
                all_variables.add(abs(lit))
        return all_variables


def normalize_clauses(clauses: list[tuple[int, ...]]) -> list[tuple[int, ...]]:

    # Normalize clauses: 1-based, vars from exactly [1, ..., n]
    normalized_clauses = []

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
        normalized_clauses.append(renamed_clause)

    return normalized_clauses


def get_instance_from_bit_matrix(matrix: np.ndarray) -> Instance:
    clauses = bit_matrix_to_clauses(matrix)
    return Instance(clauses)

