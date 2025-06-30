import pytest
from sat.solve.local_search.schoening import is_satisfiable_schoening
from test.solve.utils import get_satisfiable_instances, get_unsatisfiable_instances


@pytest.mark.parametrize("instance", get_satisfiable_instances())
def test_schoening_sat(instance):
    assert is_satisfiable_schoening(instance)


@pytest.mark.parametrize("instance", get_unsatisfiable_instances(only_small=True))
def test_schoening_unsat(instance):
    assert not is_satisfiable_schoening(instance)
