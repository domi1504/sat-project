import os
import pytest
from sat.encoding.dimacs_cnf import parse_dimacs_cnf
from sat.solve.local_search.random_local_search import is_satisfiable_random_local_search
from sat.solve.local_search.two_sided_deterministic_local_search import \
    is_satisfiable_two_sided_deterministic_local_search


# All satisfiable
directory = "../samples/uf20_91"
# Get all .cnf files in the directory
cnf_files = [f for f in sorted(os.listdir(directory)) if f.endswith(".cnf")][:100]


@pytest.mark.parametrize("filename", cnf_files)
def test_is_satisfiable_random_local_search_uf20_91(filename):
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
        result = is_satisfiable_random_local_search(inst, 1e-7)
        assert result


# All unsatisfiable
directory2 = "../samples/small_unsat"
# Get all .cnf files in the directory
# Only first ten since this takes a while
cnf_files2 = [f for f in sorted(os.listdir(directory2)) if f.endswith(".cnf")][:4]


@pytest.mark.parametrize("filename", cnf_files2)
def test_is_satisfiable_random_local_search_small_unsat(filename):
    """
    Check for every instance of the uf50_218 whether False is returned.

    :return:
    """

    file_path = os.path.join(directory2, filename)

    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

        # Parse instance
        inst = parse_dimacs_cnf(content)

        # Solve instance
        result = is_satisfiable_random_local_search(inst, 1e-7)
        assert not result


# directory3 = "../samples/uuf50_218"
# # Get all .cnf files in the directory
# # Only first ten since this takes a while
# cnf_files3 = [f for f in sorted(os.listdir(directory3)) if f.endswith(".cnf")][:10]
#
#
# @pytest.mark.parametrize("filename", cnf_files3)
# def test_is_satisfiable_schoening_uuf50_218(filename):
#     """
#     Check for every instance of the uf50_218 whether False is returned.
#
#     :return:
#     """
#
#     file_path = os.path.join(directory3, filename)
#
#     with open(file_path, 'r', encoding='utf-8') as file:
#         content = file.read()
#
#         # Parse instance
#         inst = parse_dimacs_cnf(content)
#
#         # Solve instance
#         result = is_satisfiable_schoening(inst, 1e-8)
#         assert not result
