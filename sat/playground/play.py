import time

from sat.core_attributes.renamable_horn import is_renamable_horn
from sat.core_attributes.self_sufficient_assignment import is_self_sufficient_assignment
from sat.encoding.dimacs_cnf import parse_dimacs_cnf, write_dimacs_cnf
from sat.instance.clauses.clauses import clauses_valid
from sat.modify.assign_and_simplify import assign_and_simplify
from sat.solve.brute_force import is_satisfiable_brute_force, check_assignment
import os

from sat.solve.dpll.dpll import is_satisfiable_dpll
from sat.solve.dpll.dpll_cdcl import is_satisfiable_dpll_cdcl_ncbt
from sat.solve.dpll.dpll_recursive import is_satisfiable_dpll_recursive
from sat.solve.dpll.heuristics import dlis, dlcs
from sat.solve.paturi_pudlak_zane import is_satisfiable_paturi_pudlak_zane
from sat.solve.two_sat import is_satisfiable_2_sat

file_path = './samples/uf20_91/uf20-01.cnf'
# file_path = './samples/dimacs_cnf/1.txt'
# todo. make sure variables do not get renamed when parsing dimacs?

with open(file_path, 'r') as file:
    file_content = file.read()

inst = parse_dimacs_cnf(file_content)

# res = is_satisfiable_dpll(inst, dlis)
res = is_satisfiable_paturi_pudlak_zane(inst)
print(res)

