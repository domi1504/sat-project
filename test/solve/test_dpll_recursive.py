import pytest
from sat.solve.dpll.dpll_recursive import is_satisfiable_dpll_recursive
from test.solve.utils import (
    get_satisfiable_instances,
    get_unsatisfiable_instances,
    dpll_heuristics,
)


@pytest.mark.parametrize("instance", get_satisfiable_instances())
@pytest.mark.parametrize("heuristic", dpll_heuristics)
def test_dpll_recursive_sat(instance, heuristic):
    assert is_satisfiable_dpll_recursive(instance, heuristic)


@pytest.mark.parametrize("instance", get_unsatisfiable_instances())
@pytest.mark.parametrize("heuristic", dpll_heuristics)
def test_dpll_recursive_unsat(instance, heuristic):
    assert not is_satisfiable_dpll_recursive(instance, heuristic)
