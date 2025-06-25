import pytest
from sat.solve.dpll.dpll_cdcl import is_satisfiable_dpll_cdcl_ncbt
from test.solve.utils import get_satisfiable_instances, get_unsatisfiable_instances, dpll_heuristics


@pytest.mark.parametrize("instance", get_satisfiable_instances())
@pytest.mark.parametrize("heuristic", dpll_heuristics)
def test_dpll_cdcl_sat(instance, heuristic):
    assert is_satisfiable_dpll_cdcl_ncbt(instance, heuristic)


@pytest.mark.parametrize("instance", get_unsatisfiable_instances())
@pytest.mark.parametrize("heuristic", dpll_heuristics)
def test_dpll_cdcl_unsat(instance, heuristic):
    assert not is_satisfiable_dpll_cdcl_ncbt(instance, heuristic)

