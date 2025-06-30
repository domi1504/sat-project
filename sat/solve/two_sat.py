import networkx as nx  # type: ignore
from sat.core_attributes.two_sat import is_2_sat
from sat.instance.instance import Instance


def is_satisfiable_2_sat(instance: Instance) -> bool:
    """
    Determines whether a 2-SAT instance is satisfiable using implication graphs in polynomial time.

    References:
        - Schöning p.67 f.
        - Aspvall, Plass, Tarjan: A linear-time algorithm for testing the truth of certain quantified boolean formulas.
            (1979) - https://doi.org/10.1016/0020-0190(79)90002-4

    :param instance: A 2-SAT instance.
    :return: True if the instance is satisfiable, False otherwise.
    """
    assert is_2_sat(instance), "Not a 2-SAT instance"

    # Build implication graph
    implication_graph = nx.DiGraph()

    # Two nodes per variable
    implication_graph.add_nodes_from([i + 1 for i in range(instance.num_variables)])
    implication_graph.add_nodes_from([-(i + 1) for i in range(instance.num_variables)])

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
