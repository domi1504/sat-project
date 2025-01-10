from sat.core_attributes.renamable_horn import is_renamable_horn
from sat.encoding.dimacs_cnf import syntax_check_dimacs_snf, parse_dimacs_cnf, write_dimacs_cnf
from sat.instance.clauses.clauses import clauses_valid
from sat.solve.brute_force import is_satisfiable
import os

from sat.solve.two_sat import is_satisfiable_2_sat

file_path = './samples/dimacs_cnf/2.txt'

with open(file_path, 'r') as file:
    file_content = file.read()

inst = parse_dimacs_cnf(file_content)

res = is_renamable_horn(inst)

print(res)