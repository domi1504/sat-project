import pytest
from sat.solve.dpll.paturi_pudlak_zane import is_satisfiable_paturi_pudlak_zane
from test.solve.utils import get_satisfiable_instances, get_unsatisfiable_instances


@pytest.mark.parametrize("instance", get_satisfiable_instances())
def test_ppz_sat(instance):
    assert is_satisfiable_paturi_pudlak_zane(instance, error_rate=1e-8)


@pytest.mark.parametrize("instance", get_unsatisfiable_instances(only_small=True))
def test_ppz_unsat(instance):
    assert not is_satisfiable_paturi_pudlak_zane(instance, error_rate=1e-8)
