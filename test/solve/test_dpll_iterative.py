import pytest
from sat.solve.dpll.dpll import is_satisfiable_dpll
from test.solve.utils import (
    get_satisfiable_instances,
    get_unsatisfiable_instances,
    dpll_heuristics,
)


@pytest.mark.parametrize("instance", get_satisfiable_instances())
@pytest.mark.parametrize("heuristic", dpll_heuristics)
def test_dpll_iterative_sat(instance, heuristic):
    assert is_satisfiable_dpll(instance, heuristic)[0]


@pytest.mark.parametrize("instance", get_unsatisfiable_instances())
@pytest.mark.parametrize("heuristic", dpll_heuristics)
def test_dpll_iterative_unsat(instance, heuristic):
    assert not is_satisfiable_dpll(instance, heuristic)[0]
