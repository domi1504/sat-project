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
    assert is_2_sat(instance)

    # Build implication graph
    implication_graph = nx.DiGraph()

    # Two nodes per variable
    implication_graph.add_nodes_from([f"{i+1}" for i in range(instance.nr_vars())])
    implication_graph.add_nodes_from([f"-{i+1}" for i in range(instance.nr_vars())])

    # For each clause (x, y) add 2 edges: (-x -> y), (-y, x)
    for clause in instance.clauses:
        a, b = clause[0], clause[1]
        # -a -> b
        implication_graph.add_edge(a[1:] if a.startswith("-") else f"-{a}", b)
        # -b -> a
        implication_graph.add_edge(b[1:] if b.startswith("-") else f"-{b}", a)

    # Compute strongly connected components
    sccs = list(nx.strongly_connected_components(implication_graph))

    # Check for every scc: cannot contain x and -x
    for component in sccs:
        contained_vars = set()
        for lit in component:
            contained_vars.add(lit if not lit.startswith("-") else lit[1:])
        if len(contained_vars) != len(component):
            # Found: a variable is contained in positive and negative form
            return False

    return True

