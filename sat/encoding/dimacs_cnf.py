import numpy as np
from sat.instance.instance import Instance


def syntax_check_dimacs_snf(dimacs_cnf: str):

    # todo
    pass


def parse_dimacs_cnf(dimacs_cnf: str) -> Instance:

    if not syntax_check_dimacs_snf(dimacs_cnf):
        raise Exception("Dimacs-cnf syntax check failed")

    # todo
    pass



def write_dimacs_cnf(f: Instance) -> str:
    # todo.
    pass

