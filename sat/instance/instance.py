from typing import Optional
import numpy as np
from sat.instance.bit_matrix import bit_matrix_valid, clauses_to_bit_matrix, bit_matrix_to_clauses


class Instance:
    """
    This is the class representing a boolean formula in CNF.
    """

    def __init__(self, clauses: list[tuple[int, ...]]):
        """
        Initializes the SAT instance with a list of clauses.

        Each clause is a tuple of integers representing literals.
        Literals are positive or negative integers, representing variables and their negations.

        Example:
            [(-1, 2, -3), (1, 2, 3)]
            corresponds to (!x1 ∨ x2 ∨ !x3) ∧ (x1 ∧ x2 ∧ x3)

        :param clauses: List of clauses to be saved in the instance.
        """
        self.clauses: list[tuple[int, ...]] = clauses
        assert clauses_valid(self.clauses)
        self.num_clauses: int = len(self.clauses)
        self.num_variables: int = len(self.get_all_variables())

        # Possibility to "cache" bit matrix representation of this instance
        self.bit_matrix: Optional[np.ndarray] = None

    def __str__(self):
        """
        Returns a string representation of the instance showing the number of variables and clauses.

        :return: String summary of the instance.
        """
        return f"Instance with {self.num_variables} variables and {self.num_clauses} clauses"

    def get_bit_matrix(self) -> np.ndarray:
        """
        Converts the clause representation into a bit matrix representation and caches it.
        The bit matrix is a binary representation of clauses and literals.
        :return: Numpy array representing the bit matrix.
        :raises Exception: If the instance contains empty clauses or has no clauses.
        """
        if self.bit_matrix is not None:
            return self.bit_matrix
        if len(self.clauses) > 0 and not sum(len(c) for c in self.clauses) == 0:
            self.bit_matrix = clauses_to_bit_matrix(self.clauses)
            assert bit_matrix_valid(self.bit_matrix)
            return self.bit_matrix
        else:
            raise Exception("Bit matrix not computable")

    def get_all_variables(self) -> set[int]:
        """
        Returns a set of all variable indices used in the instance.

        :return: Set of unique variable indices as positive integers.
        """
        all_variables = set()
        for clause in self.clauses:
            for lit in clause:
                all_variables.add(abs(lit))
        return all_variables

    def has_empty_clause(self) -> bool:
        """
        Checks whether the instance contains at least one empty clause.

        :return: True if any clause is empty; False otherwise.
        """
        return any(len(clause) == 0 for clause in self.clauses)

    def get_longest_clause_length(self) -> int:
        """
        Finds the length of the longest clause in the instance.

        :return: Integer representing the size of the longest clause.
        """
        return max(len(clause) for clause in self.clauses)


def clauses_valid(clauses: list[tuple[int, ...]], variables_perfectly_1_to_n: bool = False) -> bool:
    """
    Validates a list of SAT clauses.

    Each clause must be a tuple of non-zero integers, where each integer represents a literal.
    Literals are positive or negative integers corresponding to variables and their negations.

    Validation includes:
    - Ensuring all clauses are tuples
    - Ensuring all literals are integers
    - Ensuring no literal is 0

    If `variables_perfectly_1_to_n` is True, an additional check is performed:
    - All variable indices must form the exact range [1, 2, ..., n] without gaps or duplicates

    :param clauses: List of clauses, where each clause is a tuple of integer literals.
    :param variables_perfectly_1_to_n: Whether to enforce that variables form the exact sequence [1, ..., n].
    :return: True if all validation checks pass; False otherwise.
    """

    # Check datatypes
    for clause in clauses:
        if type(clause) != tuple:
            return False
        for lit in clause:
            if type(lit) != int:
                return False

    # Variables are 1-based
    for clause in clauses:
        for lit in clause:
            if lit == 0:
                return False

    if not variables_perfectly_1_to_n:
        # Do not check following property
        return True

    # Check that only variables from exactly  [1, ..., n] (not more, not less!)
    variables = set()
    for clause in clauses:
        for lit in clause:
            variables.add(abs(lit))

    variables = sorted(list(variables))
    if variables != list(range(1, len(variables) + 1)):
        return False

    # All checks succeeded
    return True


def normalize_clauses(clauses: list[tuple[int, ...]]) -> list[tuple[int, ...]]:
    """
    Normalizes clause variable indices to be contiguous and 1-based.

    Each variable in the input is remapped so that variable indices become [1, ..., n],
    where n is the number of unique variables.

    :param clauses: List of clauses with arbitrary variable indices.
    :return: List of normalized clauses with remapped variable indices.
    """

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
    """
    Creates an Instance object from a bit matrix representation.

    This function converts the bit matrix back to clauses using `bit_matrix_to_clauses`,
    and then constructs an Instance.

    :param matrix: Bit matrix representing a SAT instance.
    :return: An Instance object reconstructed from the matrix.
    """
    clauses = bit_matrix_to_clauses(matrix)
    return Instance(clauses)

