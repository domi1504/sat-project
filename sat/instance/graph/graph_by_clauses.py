import numpy as np
import networkx as nx
from sat.instance.instance import Instance

"""
Graph by clauses

1 node per clause
Edge between two nodes (clauses), if they share a variable (pos or neg form) 

E.g.
(x1 or x2) and (!x2 or x3) and (x3 or x4)
===
(A) --- (B) --- (C)
"""

def create_graph_by_clauses(instance: Instance) -> nx.Graph:

    g = nx.Graph()

    # One node per clause
    g.add_nodes_from(list(range(instance.num_clauses)))

    # Add edges

    # Look at all distinct clause pairs
    for i in range(instance.num_clauses - 1):
        for j in range(i + 1, instance.num_clauses):

            shared_variables = []

            # For each variable: check if it is contained in both clauses
            for k in range(instance.num_variables):
                if 1 in instance.bit_matrix[i, 2 * k : 2 * k + 2] and 1 in instance.bit_matrix[j, 2 * k : 2 * k + 2]:
                    shared_variables.append(str(k))

            if len(shared_variables) > 0:
                g.add_edge(i, j, shared_variables=','.join(shared_variables))

    return g

def create_multi_graph_by_clauses(instance: Instance) -> nx.MultiGraph:
    """
    One edge per shared variable.
    :param instance:
    :return:
    """

    g = nx.MultiGraph()

    # One node per clause
    g.add_nodes_from(list(range(instance.num_clauses)))

    # Add edges

    # Look at all distinct clause pairs
    for i in range(instance.num_clauses - 1):
        for j in range(i + 1, instance.num_clauses):

            # For each variable: check if it is contained in both clauses
            for k in range(instance.num_variables):
                if 1 in instance.bit_matrix[i, 2 * k : 2 * k + 2] and 1 in instance.bit_matrix[j, 2 * k : 2 * k + 2]:
                    g.add_edge(i, j, shared_variable=k)

    return g

