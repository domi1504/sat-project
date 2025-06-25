import pytest
from sat.solve.local_search.greedy_sat import is_satisfiable_gsat
from test.solve.utils import get_satisfiable_instances, get_unsatisfiable_instances


@pytest.mark.parametrize("instance", get_satisfiable_instances())
def test_gsat_sat(instance):
    assert is_satisfiable_gsat(instance)


@pytest.mark.parametrize("instance", get_unsatisfiable_instances(only_small=True))
def test_gsat_unsat(instance):
    assert not is_satisfiable_gsat(instance)

