import time

from sat.generate.generate_random_k_sat import generate_random_k_sat_instance
from sat.instance.instance import Instance
from sat.solve.brute_force import is_satisfiable_brute_force
from sat.solve.dpll.dpll_cdcl import is_satisfiable_dpll_cdcl_ncbt
from sat.solve.dpll.heuristics import dlis
from sat.solve.local_search.greedy_sat import is_satisfiable_gsat
from sat.solve.local_search.greedy_sat_with_walk import is_satisfiable_gsat_with_walk
import json

from sat.solve.local_search.schoening import is_satisfiable_schoening
from sat.solve.local_search.walk_sat import is_satisfiable_wsat

k = 3
NR_SAMPLES = 100
GAMMAS = [4.26]
N_RANGE = range(3, 51)

timestamp = time.time()

ALGOS = [
    # is_satisfiable_brute_force,
    # lambda inst: is_satisfiable_gsat(inst, max_tries=2 ** inst.num_variables),
    # lambda inst: is_satisfiable_gsat_with_walk(inst, max_tries=2 ** inst.num_variables),
    # lambda inst: is_satisfiable_wsat(inst, max_tries=2 ** inst.num_variables),
    is_satisfiable_schoening,
]
ALGO_NAMES = [
    # "bruteforce",
    # "gsat",
    # "gsat-walk",
    # "wsat",
    "schoening"
]

for ALGO, ALGO_NAME in zip(ALGOS, ALGO_NAMES):

    sat_results: dict = {}

    for gamma in GAMMAS:
        sat_results[gamma] = {}
        for n in N_RANGE:
            print(f"algo: {ALGO_NAME}, gamma: {gamma}, n: {n}")
            sat_results[gamma][n] = []
            while len(sat_results[gamma][n]) < NR_SAMPLES:
                instance = generate_random_k_sat_instance(n, int(gamma * n), k)
                if is_satisfiable_dpll_cdcl_ncbt(instance, dlis)[0]:
                    res, nr_its = ALGO(instance)
                    sat_results[gamma][n].append(nr_its)

    # At the end of the script, write out the results
    with open(f"sat_results_50_{ALGO_NAME}.json", "w") as f:
        json.dump(sat_results, f, indent=4)
