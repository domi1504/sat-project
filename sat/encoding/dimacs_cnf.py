from sat.instance.instance import Instance, normalize_clauses
import re


"""
See: https://jix.github.io/varisat/manual/0.2.0/formats/dimacs.html
My additions: 
    - multiple spaces are replaced to one space before parsing.
    - if a '%' appears at the end of the file, it gets removed

DIMACS CNF format:

c This is a comment
p cnf <num_vars> <num_clauses>
1 2 0
-2 -3 0
-1 3 0

"""


def _syntax_check_dimacs_snf(lines: list[str]):

    # Check first line for format "p cnf <INT> <INT>"
    if not re.match(r"^p cnf [1-9]\d* [1-9]\d*$", lines[0]):
        return False

    num_variables, num_clauses = lines[0][6:].split(" ")
    num_variables = int(num_variables)
    num_clauses = int(num_clauses)

    # Check number of lines
    if len(lines) != num_clauses + 1:
        return False

    # Check rest of lines:
    for line in lines[1:]:
        if not re.match(r"^(-?\d+\s)*-?\d+\s0$", line):
            return False

    # Check for matching number of variables
    all_vars = set()
    for line in lines[1:]:
        lits = line.split(" ")[:-1]
        for lit in lits:
            if lit.startswith("-"):
                all_vars.add(lit[1:])
            else:
                all_vars.add(lit)

    if len(all_vars) != num_variables:
        return False

    return True


def parse_dimacs_cnf(dimacs_cnf: str) -> Instance:

    # Replace multiple spaces with one space
    dimacs_cnf = re.sub(r' {2,}', ' ', dimacs_cnf)

    # Get separate lines
    lines = dimacs_cnf.strip().split("\n")

    # Strip all lines
    lines = list(line.strip() for line in lines)

    # Remove comments
    lines = list(line for line in lines if not line.startswith("c"))

    # Check if some line with "%" appears
    for i in range(len(lines)):
        if '%' in lines[i]:
            # If so: delete everything from that line on
            lines = lines[:i]
            break

    if not _syntax_check_dimacs_snf(lines):
        raise Exception("Dimacs-cnf syntax check failed")

    # Parse clauses
    clauses = set()
    for line in lines[1:]:
        # Parse clause
        clause_as_str = tuple(line.split(" ")[:-1])
        clause = tuple(int(lit) for lit in clause_as_str)
        clauses.add(clause)

    return Instance(normalize_clauses(clauses))


def write_dimacs_cnf(instance: Instance) -> str:

    num_clauses = instance.num_clauses
    num_variables = instance.num_variables

    # Write header
    dimacs_cnf = f"p cnf {num_variables} {num_clauses}"

    # Write clause lines
    for clause in instance.clauses:
        line = ""
        for lit in clause:
            line += f"{lit} "
        line += "0"
        dimacs_cnf += "\n" + line

    return dimacs_cnf

