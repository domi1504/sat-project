import pytest
from sat.solve.local_search.dantsin_local_search import (
    is_satisfiable_dantsin_local_search,
)
from test.solve.utils import get_satisfiable_instances, get_unsatisfiable_instances


@pytest.mark.parametrize("instance", get_satisfiable_instances(only_small=True))
def test_dantsin_sat(instance):
    assert is_satisfiable_dantsin_local_search(instance)


@pytest.mark.parametrize("instance", get_unsatisfiable_instances(only_small=True))
def test_dantsin_unsat(instance):
    assert not is_satisfiable_dantsin_local_search(instance)
