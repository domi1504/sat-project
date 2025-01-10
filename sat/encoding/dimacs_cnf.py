from sat.instance.bit_matrix.bit_matrix import clauses_to_bit_matrix
from sat.instance.instance import Instance
import re


"""
See: https://jix.github.io/varisat/manual/0.2.0/formats/dimacs.html

DIMACS CNF format:

c This is a comment
p cnf <num_vars> <num_clauses>
1 2 0
-2 -3 0
-1 3 0

"""


def syntax_check_dimacs_snf(dimacs_cnf: str):

    # Get separate lines
    lines = dimacs_cnf.strip().split("\n")

    # Remove comments
    lines = list(line for line in lines if not line.startswith("c"))

    # Check first line for format "p cnf <INT> <INT>"
    if not re.match(r"^p cnf [1-9]\d* [1-9]\d*$", lines[0].strip()):
        return False

    num_variables, num_clauses = lines[0][6:].split(" ")
    num_variables = int(num_variables)
    num_clauses = int(num_clauses)

    # Check number of lines
    if len(lines) != num_clauses + 1:
        return False

    # Check rest of lines:
    for line in lines[1:]:
        if not re.match(r"^(-?\d+\s)*-?\d+\s0$", line.strip()):
            return False

    # Check for matching number of variables
    all_vars = set()
    for line in lines[1:]:
        lits = line.strip().split(" ")[:-1]
        for lit in lits:
            if lit.startswith("-"):
                all_vars.add(lit[1:])
            else:
                all_vars.add(lit)

    if len(all_vars) != num_variables:
        return False

    return True


def parse_dimacs_cnf(dimacs_cnf: str) -> Instance:

    if not syntax_check_dimacs_snf(dimacs_cnf):
        raise Exception("Dimacs-cnf syntax check failed")

    # Get separate lines
    lines = dimacs_cnf.strip().split("\n")

    # Remove comments
    lines = list(line for line in lines if not line.startswith("c"))

    # Parse clauses
    clauses = set()
    for line in lines[1:]:
        clauses.add(tuple(line.strip(" ").split(" ")[:-1]))

    # Compute bit matrix
    bit_matrix = clauses_to_bit_matrix(clauses)

    return Instance(bit_matrix)


def write_dimacs_cnf(instance: Instance) -> str:

    num_clauses = instance.nr_clauses()
    num_variables = instance.nr_vars()

    # Write header
    dimacs_cnf = f"p cnf {num_variables} {num_clauses}"

    # Write clause lines
    for clause in instance.clauses:
        line = ""
        for lit in clause:
            line += lit + " "
        line += "0"
        dimacs_cnf += "\n" + line

    return dimacs_cnf

