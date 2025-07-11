from sat.instance.instance import Instance, normalize_clauses
import re


"""
DIMACS CNF Format Parser and Serializer for SAT Instances

Supports reading and writing SAT problem instances using the standard
DIMACS CNF format, with some preprocessing enhancements.

Enhancements:
- Multiple consecutive spaces are normalized to a single space.
- Lines after a line containing '%' are removed.
- Comments starting with 'c' are ignored.

Reference: https://jix.github.io/varisat/manual/0.2.0/formats/dimacs.html
"""


def _syntax_check_dimacs_snf(lines: list[str]):
    """
    Performs a syntax check on the lines of a DIMACS CNF file (excluding comments).

    Validates:
    - The first line starts with "p cnf <num_vars> <num_clauses>"
    - The number of clause lines matches the header
    - Each clause line ends with '0' and contains valid integer literals
    - The declared number of variables matches the distinct variables used

    :param lines: List of non-comment lines from a DIMACS CNF file.
    :return: True if the syntax is valid; False otherwise.
    """

    # Check first line for format "p cnf <INT> <INT>"
    if not re.match(r"^p cnf [1-9]\d* [1-9]\d*$", lines[0]):
        return False

    num_variables, num_clauses = map(int, lines[0][6:].split(" "))

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
    """
    Parses a DIMACS CNF formatted string into an `Instance` object.

    Steps:
    - Removes comments and any line following a '%' character
    - Normalizes whitespace
    - Validates syntax
    - Converts clauses to tuples of integers
    - Normalizes variable indices to [1, ..., n]

    :param dimacs_cnf: String in DIMACS CNF format.
    :return: An `Instance` object representing the SAT problem.
    :raises Exception: If the input string fails the DIMACS syntax validation.
    """

    # Replace multiple spaces with one space
    dimacs_cnf = re.sub(r" {2,}", " ", dimacs_cnf)

    # Get separate lines
    lines = dimacs_cnf.strip().split("\n")

    # Strip all lines
    lines = list(line.strip() for line in lines)

    # Remove comments
    lines = list(line for line in lines if not line.startswith("c"))

    # Check if some line with "%" appears
    for i in range(len(lines)):
        if "%" in lines[i]:
            # If so: delete everything from that line on
            lines = lines[:i]
            break

    if not _syntax_check_dimacs_snf(lines):
        raise Exception("Dimacs-cnf syntax check failed")

    # Parse clauses
    clauses = []
    for line in lines[1:]:
        # Parse clause
        clause_as_str = tuple(line.split(" ")[:-1])
        clause = tuple(int(lit) for lit in clause_as_str)
        clauses.append(clause)

    return Instance(normalize_clauses(clauses))


def write_dimacs_cnf(instance: Instance) -> str:
    """
    Serializes an `Instance` object into a DIMACS CNF formatted string.

    Each clause is written on its own line, ending with a '0'.
    Includes a header line of the form: `p cnf <num_vars> <num_clauses>`

    :param instance: An `Instance` representing a SAT problem.
    :return: A string in DIMACS CNF format suitable for saving or exporting.
    """

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
