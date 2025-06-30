import pytest
from sat.solve.local_search.greedy_sat_with_walk import is_satisfiable_gsat_with_walk
from test.solve.utils import get_satisfiable_instances, get_unsatisfiable_instances


@pytest.mark.parametrize("instance", get_satisfiable_instances(only_small=True))
def test_gsat_with_walk_sat(instance):
    assert is_satisfiable_gsat_with_walk(instance)


@pytest.mark.parametrize("instance", get_unsatisfiable_instances(only_small=True))
def test_gsat_with_walk_unsat(instance):
    assert not is_satisfiable_gsat_with_walk(instance, max_tries=100)
