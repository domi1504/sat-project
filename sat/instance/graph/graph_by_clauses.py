import numpy as np
import networkx as nx
from sat.instance.instance import Instance


def create_graph_by_clauses(instance: Instance) -> nx.Graph:

    # Matrix: #clauses x #variables
    var_occs = np.zeros((instance.bit_matrix.shape[0], instance.bit_matrix.shape[1] // 2), dtype=np.uint8)
    for i in range(var_occs.shape[0]):
        for j in range(var_occs.shape[1]):
            var_occs[i, j] = instance.bit_matrix[i, 2 * j] or instance.bit_matrix[i, 2 * j + 1]

    g = nx.Graph()

    # One node per clause
    g.add_nodes_from(list(range(instance.nr_clauses())))

    # Add edges
    for i in range(instance.nr_clauses()):
        for j in range(instance.nr_clauses()):

            if i == j:
                continue

            if 2 in (var_occs[i] + var_occs[j]):
                if (i, j) not in g.edges:
                    g.add_edge(i, j)

    return g
