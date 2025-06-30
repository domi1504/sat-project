import pytest
from sat.solve.local_search.two_sided_deterministic_local_search import (
    is_satisfiable_two_sided_deterministic_local_search,
)
from test.solve.utils import get_satisfiable_instances, get_unsatisfiable_instances


@pytest.mark.parametrize("instance", get_satisfiable_instances())
def test_two_sided_det_local_search_sat(instance):
    assert is_satisfiable_two_sided_deterministic_local_search(instance)


@pytest.mark.parametrize("instance", get_unsatisfiable_instances(only_small=True))
def test_two_sided_det_local_search_unsat(instance):
    assert not is_satisfiable_two_sided_deterministic_local_search(instance)
