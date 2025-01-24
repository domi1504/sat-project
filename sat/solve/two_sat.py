import networkx as nx
from sat.core_attributes.two_sat import is_2_sat
from sat.instance.instance import Instance


"""
Referenz siehe Schöning
O(n + m), je nach Implementierung von strongly connected components
"""


def is_satisfiable_2_sat(instance: Instance) -> bool:
    """
    :param instance:
    :return:
    """
    assert is_2_sat(instance), "Not a 2-SAT instance"

    # Build implication graph
    implication_graph = nx.DiGraph()

    # Two nodes per variable
    implication_graph.add_nodes_from([i+1 for i in range(instance.num_variables)])
    implication_graph.add_nodes_from([-(i+1) for i in range(instance.num_variables)])

    # For each clause (x, y) add 2 edges: (-x -> y), (-y, x)
    for clause in instance.clauses:
        a, b = clause[0], clause[1]
        # -a -> b
        implication_graph.add_edge(-a, b)
        # -b -> a
        implication_graph.add_edge(-b, a)

    # Compute strongly connected components
    sccs = list(nx.strongly_connected_components(implication_graph))

    # Check for every scc: cannot contain x and -x
    for component in sccs:
        contained_vars = set()
        for lit in component:
            contained_vars.add(abs(lit))
        if len(contained_vars) != len(component):
            # Found: a variable x that is contained in positive and negative form
            return False

    return True

