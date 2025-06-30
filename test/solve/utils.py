import os
from typing import Iterator
from sat.encoding.dimacs_cnf import parse_dimacs_cnf
from sat.instance.instance import Instance
from sat.solve.dpll.heuristics import (
    jeroslaw_wang,
    jeroslaw_wang_two_sided,
    shortest_clause,
    dlis,
    dlcs,
    rdlcs,
    mom,
    DPLLHeuristic,
)


dpll_heuristics: list[DPLLHeuristic] = [
    dlis,
    dlcs,
    rdlcs,
    mom,
    jeroslaw_wang,
    jeroslaw_wang_two_sided,
    shortest_clause,
]


def load_instances_from(directory: str, limit: int) -> Iterator[Instance]:
    cnf_files = [f for f in sorted(os.listdir(directory)) if f.endswith(".cnf")][:limit]
    for filename in cnf_files:
        file_path = os.path.join(directory, filename)
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()
            yield parse_dimacs_cnf(content)


def get_satisfiable_instances(only_small: bool = False) -> Iterator[Instance]:
    yield from load_instances_from("../samples/small_sat", 25)
    if not only_small:
        yield from load_instances_from("../samples/uf20_91", 100)


def get_unsatisfiable_instances(only_small: bool = False) -> Iterator[Instance]:
    yield from load_instances_from("../samples/small_unsat", 25)
    if not only_small:
        yield from load_instances_from("../samples/uuf50_218", 5)
