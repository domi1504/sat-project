from sat.encoding.dimacs_cnf import parse_dimacs_cnf, write_dimacs_cnf

from sat.solve.dpll.dpll import is_satisfiable_dpll
from sat.solve.dpll.heuristics import dlis, dlcs
from sat.solve.local_search.cover_code import generate_cover_code_greedy, generate_cover_code, self_concatenate
from sat.solve.local_search.dantsin_local_search import is_satisfiable_dantsin_local_search
from sat.solve.schoening import is_satisfiable_schoening

# folder_path = './samples/temp'
file_path = './samples/uf20_91/uf20-01.cnf'
# todo. make sure variables do not get renamed when parsing dimacs?


a = generate_cover_code(11, 0.25)
print(len(a))


with open(file_path, 'r') as file:
    file_content = file.read()
inst = parse_dimacs_cnf(file_content)

res = is_satisfiable_dantsin_local_search(inst)
print(res)

