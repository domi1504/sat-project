from sat.encoding.dimacs_cnf import parse_dimacs_cnf, write_dimacs_cnf
from sat.generate.generate_random_k_sat import generate_random_k_sat_instance
from sat.solve.brute_force import is_satisfiable_brute_force
from sat.solve.dpll.dpll_cdcl import is_satisfiable_dpll_cdcl_ncbt
from sat.solve.dpll.heuristics import dlis
from sat.solve.dpll.paturi_pudlak_zane import is_satisfiable_paturi_pudlak_zane

from sat.solve.local_search.cover_code import generate_cover_code
from sat.solve.local_search.dantsin_local_search import (
    is_satisfiable_dantsin_local_search,
)
from sat.solve.local_search.greedy_sat import is_satisfiable_gsat

# folder_path = './samples/temp'
file_path = "./samples/small_unsat/small-unsat-1.cnf"
# todo. make sure variables do not get renamed when parsing dimacs?


# with open(file_path, "r") as file:
#     file_content = file.read()
# inst = parse_dimacs_cnf(file_content)

instance = generate_random_k_sat_instance(100, 500, 3)

res = is_satisfiable_dpll_cdcl_ncbt(instance, dlis)

print(res)
