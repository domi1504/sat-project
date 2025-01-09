from sat.encoding.bit_matrix import parse_bit_matrix, write_bit_matrix
from sat.encoding.dimacs_cnf import syntax_check_dimacs_snf, parse_dimacs_cnf, write_dimacs_cnf
from sat.solve.brute_force import is_satisfiable

"""
file_path = '../../samples/is_core/1.txt'
with open(file_path, 'r') as file:
    file_content = file.read()
instance = parse_bit_matrix(file_content)
print(instance.bit_matrix)
print(".")
print(instance.clauses)
print(write_bit_matrix(instance))
"""


file_path = '../../samples/dimacs_cnf/2.txt'

with open(file_path, 'r') as file:
    file_content = file.read()

inst = parse_dimacs_cnf(file_content)


# print(inst.clauses)

print(" ")

# print(write_dimacs_cnf(inst))

res = is_satisfiable(inst)
print(res)
