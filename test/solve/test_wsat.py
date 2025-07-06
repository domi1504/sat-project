import pytest
from sat.solve.local_search.walk_sat import is_satisfiable_wsat
from test.solve.utils import get_satisfiable_instances, get_unsatisfiable_instances


@pytest.mark.parametrize("instance", get_satisfiable_instances(only_small=True))
def test_wsat_sat(instance):
    assert is_satisfiable_wsat(instance)[0]


@pytest.mark.parametrize("instance", get_unsatisfiable_instances(only_small=True))
def test_wsat_unsat(instance):
    assert not is_satisfiable_wsat(instance, max_tries=100)[0]
