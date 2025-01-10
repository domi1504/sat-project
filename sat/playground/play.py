from sat.encoding.dimacs_cnf import syntax_check_dimacs_snf, parse_dimacs_cnf, write_dimacs_cnf
from sat.solve.brute_force import is_satisfiable
import os

from sat.solve.two_sat import is_satisfiable_2_sat

file_path = './samples/dimacs_cnf/2sat2.txt'

with open(file_path, 'r') as file:
    file_content = file.read()

inst = parse_dimacs_cnf(file_content)

# print(inst.bit_matrix)

res = is_satisfiable(inst)
print(res)


res2 = is_satisfiable_2_sat(inst)
print(res2)