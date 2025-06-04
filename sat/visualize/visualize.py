import matplotlib.pyplot as plt
import numpy as np

from sat.encoding.bit_matrix import parse_bit_matrix
from sat.encoding.dimacs_cnf import parse_dimacs_cnf
from sat.instance.instance import Instance
from sat.visualize.bit_matrix import visualize_two_formulas
from sat.visualize.graph_by_clauses import visualize_graph_by_clauses

if __name__ == "__main__":

    file_path = '../../samples/is_core/1.txt'

    with open(file_path, 'r') as file:
        file_content = file.read()

    inst = parse_bit_matrix(file_content)

    # visualize_two_formulas(inst, inst)
    visualize_graph_by_clauses(inst)

