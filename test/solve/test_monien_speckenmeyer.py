import os
import pytest
from sat.encoding.dimacs_cnf import parse_dimacs_cnf
from sat.solve.monien_speckenmeyer import is_satisfiable_monien_speckenmeyer

# All satisfiable
directory = "../samples/uf20_91"
# Get all .cnf files in the directory
cnf_files = [f for f in sorted(os.listdir(directory)) if f.endswith(".cnf")][:100]

@pytest.mark.parametrize("filename", cnf_files)
def test_is_satisfiable_ms_uf20_91(filename):
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
        result = is_satisfiable_monien_speckenmeyer(inst)
        assert result == True


# All unsatisfiable
directory2 = "../samples/uuf50_218"
# Get all .cnf files in the directory
# Only first ten since this takes a while
cnf_files2 = [f for f in sorted(os.listdir(directory2)) if f.endswith(".cnf")][:10]

@pytest.mark.parametrize("filename", cnf_files2)
def test_is_satisfiable_ms_uuf50_218(filename):
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
        result = is_satisfiable_monien_speckenmeyer(inst)
        assert result == False
