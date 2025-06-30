import networkx as nx  # type: ignore
from sat.instance.graph.graph_by_clauses import create_graph_by_clauses
from sat.instance.instance import Instance


def is_one_connected_component(instance: Instance) -> bool:
    """
    Check whether the given formula forms a single connected component (qualifying to be a kernel instance).

    This determines if the instance can be split into multiple independent SAT sub-instances.
    For example, the formula (a, ¬b, c) AND (b, ¬c) AND (e, f) can be split into:
        [(a, ¬b, c) AND (b, ¬c)]  and  [(e, f)]

    :return:
        True  --> only one connected component.
        False --> not a kernel instance; the formula can be partitioned into two or more independent sub-instances.
    """
    g = create_graph_by_clauses(instance)
    return nx.number_connected_components(g) == 1
