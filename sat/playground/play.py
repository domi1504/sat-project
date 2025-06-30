from sat.encoding.dimacs_cnf import parse_dimacs_cnf
from sat.solve.brute_force import is_satisfiable_brute_force

from sat.solve.local_search.cover_code import generate_cover_code
from sat.solve.local_search.dantsin_local_search import (
    is_satisfiable_dantsin_local_search,
)

# folder_path = './samples/temp'
file_path = "./samples/dimacs_cnf/1.txt"
# todo. make sure variables do not get renamed when parsing dimacs?


with open(file_path, "r") as file:
    file_content = file.read()
inst = parse_dimacs_cnf(file_content)

res = is_satisfiable_brute_force(inst)
print(res)
