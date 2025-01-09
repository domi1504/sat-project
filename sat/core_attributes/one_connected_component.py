import networkx as nx
from sat.instance.graph.graph_by_clauses import create_graph_by_clauses
from sat.instance.instance import Instance


def is_one_connected_component(instance: Instance) -> bool:
    """
    Check whether given formula is a core instance.
    Check whether it can be split up into several independent SAT instances.
    E.g: (a, !b, c) AND (b, !c) AND (e, f) can be into
        [(a, !b, c) AND (b, !c)] && [(e, f)]

    :return:
        true <--> core-instance,
        false <--> not core-instance, could be split up into >= 2 smaller instances.
    """
    g = create_graph_by_clauses(instance)
    return nx.number_connected_components(g) == 1
