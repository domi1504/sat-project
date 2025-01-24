import time

from sat.core_attributes.renamable_horn import is_renamable_horn
from sat.encoding.dimacs_cnf import parse_dimacs_cnf, write_dimacs_cnf
from sat.instance.clauses.clauses import clauses_valid
from sat.modify.assign_and_simplify import assign_and_simplify
from sat.solve.brute_force import is_satisfiable_brute_force
import os

from sat.solve.dpll.dpll import is_satisfiable_dpll
from sat.solve.dpll.heuristics import dlis
from sat.solve.two_sat import is_satisfiable_2_sat

file_path = './samples/uf20_91/uf20-01.cnf'

with open(file_path, 'r') as file:
    file_content = file.read()

inst = parse_dimacs_cnf(file_content)

t = time.time()
is_satisfiable_brute_force(inst)

print(f"Brute force took {time.time() - t} ")
t = time.time()

is_satisfiable_dpll(inst, dlis)
print(f"DPLL-dlis took {time.time() - t} ")
