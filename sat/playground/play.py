from sat.encoding.dimacs_cnf import parse_dimacs_cnf, write_dimacs_cnf

from sat.solve.dpll.dpll import is_satisfiable_dpll
from sat.solve.dpll.heuristics import dlis, dlcs
from sat.solve.schoening import is_satisfiable_schoening

# folder_path = './samples/temp'
file_path = './samples/uuf50_218/uuf50-01.cnf'
# todo. make sure variables do not get renamed when parsing dimacs?

with open(file_path, 'r') as file:
    file_content = file.read()
inst = parse_dimacs_cnf(file_content)
res = is_satisfiable_schoening(inst, 1e-2)
print(res)

