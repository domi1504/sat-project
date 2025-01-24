import os
import pytest
from sat.encoding.dimacs_cnf import parse_dimacs_cnf
from sat.solve.dpll.dpll import is_satisfiable_dpll
from sat.solve.dpll.heuristics import jeroslaw_wang, jeroslaw_wang_two_sided, shortest_clause, dlis, dlcs, rdlcs, mom


directory = "../samples/uf20_91"

# Get all .cnf files in the directory
cnf_files = [f for f in sorted(os.listdir(directory)) if f.endswith(".cnf")]

heuristics = [dlis, dlcs, rdlcs, mom, jeroslaw_wang, jeroslaw_wang_two_sided, shortest_clause]


@pytest.mark.parametrize("filename", cnf_files)
@pytest.mark.parametrize("heuristic", heuristics)
def test_is_satisfiable_dpll_uf20_91(filename, heuristic):
    """
    Check for every instance of the uf20_91 whether True is returned.

    :return:
    """

    file_path = os.path.join(directory, filename)

    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

        # Parse instance
        inst = parse_dimacs_cnf(content)

        # Solve instance
        result = is_satisfiable_dpll(inst, heuristic)
        assert result == True
