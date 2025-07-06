import time
import json
from functools import partial
from multiprocessing import Pool, cpu_count

from sat.generate.generate_random_k_sat import generate_random_k_sat_instance
from sat.solve.brute_force import is_satisfiable_brute_force
from sat.solve.dpll.dpll_cdcl import is_satisfiable_dpll_cdcl_ncbt
from sat.solve.dpll.heuristics import dlis
from sat.solve.local_search.greedy_sat import is_satisfiable_gsat
from sat.solve.local_search.greedy_sat_with_walk import is_satisfiable_gsat_with_walk
from sat.solve.local_search.schoening import is_satisfiable_schoening
from sat.solve.local_search.walk_sat import is_satisfiable_wsat


def gsat_wrapper(inst):
    return is_satisfiable_gsat(inst, max_tries=2**inst.num_variables)


def gsat_walk_wrapper(inst):
    return is_satisfiable_gsat_with_walk(inst, max_tries=2**inst.num_variables)


def wsat_wrapper(inst):
    return is_satisfiable_wsat(inst, max_tries=2**inst.num_variables)


def process_one_n(n, gamma, NR_SAMPLES, ALGO):
    results = []
    while len(results) < NR_SAMPLES:
        inst = generate_random_k_sat_instance(n, int(gamma * n), 3)
        sat, _ = is_satisfiable_dpll_cdcl_ncbt(inst, dlis)
        if sat:
            _, iters = ALGO(inst)
            results.append(iters)
    return n, results


def run_for_algo(ALGO, ALGO_NAME, GAMMAS, N_RANGE, NR_SAMPLES):
    sat_results = {g: {} for g in GAMMAS}

    with Pool(cpu_count()) as pool:
        for gamma in GAMMAS:
            func = partial(process_one_n, gamma=gamma, NR_SAMPLES=NR_SAMPLES, ALGO=ALGO)
            jobs = [(n,) for n in N_RANGE]
            # starmap over n, passing gamma, NR_SAMPLES, ALGO via partial
            output = pool.starmap(func, [(n,) for n in N_RANGE])
            for n, results in output:
                sat_results[gamma][n] = results

    # Write out results per algorithm
    with open(f"sat_results_50_{ALGO_NAME}.json", "w") as f:
        json.dump(sat_results, f, indent=4)
    print(f"✅ Done: {ALGO_NAME}")


if __name__ == "__main__":
    start = time.time()

    NR_SAMPLES = 100
    GAMMAS = [4.26]
    N_RANGE = range(3, 51)

    ALGOS = [
        gsat_wrapper,
        gsat_walk_wrapper,
        wsat_wrapper,
        is_satisfiable_schoening,
    ]
    ALGO_NAMES = ["gsat", "gsat-walk", "wsat", "schoening"]

    for ALGO, ALGO_NAME in zip(ALGOS, ALGO_NAMES):
        run_for_algo(ALGO, ALGO_NAME, GAMMAS, N_RANGE, NR_SAMPLES)

    print("Total time:", time.time() - start)
