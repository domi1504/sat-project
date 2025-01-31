import time

from sat.core_attributes.renamable_horn import is_renamable_horn
from sat.core_attributes.self_sufficient_assignment import is_self_sufficient_assignment
from sat.encoding.dimacs_cnf import parse_dimacs_cnf, write_dimacs_cnf
from sat.instance.clauses.clauses import clauses_valid
from sat.modify.assign_and_simplify import assign_and_simplify
from sat.solve.brute_force import is_satisfiable_brute_force
import os

from sat.solve.dpll.dpll import is_satisfiable_dpll
from sat.solve.dpll.heuristics import dlis
from sat.solve.two_sat import is_satisfiable_2_sat

file_path = './samples/dimacs_cnf/2.txt'

with open(file_path, 'r') as file:
    file_content = file.read()

inst = parse_dimacs_cnf(file_content)

is_self_sufficient_assignment(inst, {9: False, 10: True})

# todo. make sure variables do not get renamed when parsing dimacs?