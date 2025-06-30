from sat.encoding.dimacs_cnf import write_dimacs_cnf
from sat.generate.generate_random_k_sat import generate_random_k_sat_instance
from sat.solve.brute_force import is_satisfiable_brute_force

counter = 1

while counter <= 100:

    instance = generate_random_k_sat_instance(10, 50, 3)

    if instance.num_variables != 10:
        continue

    if not is_satisfiable_brute_force(instance):
        with open(f"./samples/small_unsat/small-unsat-{counter}.cnf", "w") as text_file:
            text_file.write(write_dimacs_cnf(instance))
        counter += 1
