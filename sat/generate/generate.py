import numpy as np
from random import randrange

from sat.instance.instance import Instance

"""
todo.
def generate_random_formula_a(nr_clauses, nr_vars) -> Instance:

    while True:
        f1 = Instance(np.random.randint(2, size=(nr_clauses * 2, 2 * nr_vars)))
        f2 = normalize_formula(f1.bit_matrix)

        if f2.shape[0] >= nr_clauses and f2.shape[1] == 2*nr_vars:
            assert is_formula_normalized(f2)
            return Formula(f2[:nr_clauses+1, :])


def generate_random_formula_b(nr_clauses, nr_vars) -> Formula:

    c = 0
    while True:
        c += 1

        m = np.zeros((nr_clauses * 2, nr_vars * 2))
        for i in range(nr_clauses * 2):
            for j in range(nr_vars):
                r = randrange(3)
                if r == 0:
                    m[i, 2*j] = 0
                    m[i, 2*j+1] = 0
                elif r == 1:
                    m[i, 2 * j] = 1
                    m[i, 2 * j + 1] = 0
                else:
                    m[i, 2 * j] = 0
                    m[i, 2 * j + 1] = 1

        f1 = Formula(m)
        f2 = normalize_formula(f1.matrix)

        if f2.shape[0] >= nr_clauses and f2.shape[1] == 2*nr_vars:
            assert is_formula_normalized(f2)
            return Formula(f2[:nr_clauses+1, :])
"""