import pytest
from sat.solve.dpll.monien_speckenmeyer import is_satisfiable_monien_speckenmeyer
from test.solve.utils import get_satisfiable_instances, get_unsatisfiable_instances


# Turn self-sufficient assignment check on/off
self_sufficient_assignment_checks = [False]


@pytest.mark.parametrize("instance", get_satisfiable_instances())
@pytest.mark.parametrize(
    "self_sufficient_assignment_check", self_sufficient_assignment_checks
)
def test_monien_speckenmeyer_sat(instance, self_sufficient_assignment_check):
    assert is_satisfiable_monien_speckenmeyer(
        instance, self_sufficient_assignment_check
    )[0]


@pytest.mark.parametrize("instance", get_unsatisfiable_instances())
@pytest.mark.parametrize(
    "self_sufficient_assignment_check", self_sufficient_assignment_checks
)
def test_monien_speckenmeyer_unsat(instance, self_sufficient_assignment_check):
    assert not is_satisfiable_monien_speckenmeyer(
        instance, self_sufficient_assignment_check
    )[0]
