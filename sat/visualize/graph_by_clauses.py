from sat.encoding.bit_matrix import parse_bit_matrix
from sat.instance.graph.graph_by_clauses import create_graph_by_clauses, create_multi_graph_by_clauses
from sat.instance.instance import Instance
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np


def label_to_color(label, max_label=20, cmap_name='rainbow'):
    """
    Map an integer label to a color from a matplotlib colormap.

    Args:
        label (int): The integer label to map.
        max_label (int): The maximum label value expected.
        cmap_name (str): Name of the matplotlib colormap to use.

    Returns:
        color: RGBA tuple for matplotlib.
    """
    cmap = plt.get_cmap(cmap_name)
    # Normalize label to [0, 1]
    norm_label = label / max_label
    return cmap(norm_label)


def visualize_graph_by_clauses(instance: Instance):

    graph: nx.Graph = create_graph_by_clauses(instance)

    # Get positions for the nodes in a circular layout
    pos = nx.circular_layout(graph)

    # Draw the graph
    nx.draw_networkx(
        graph,
        pos,
        node_color='#274C77',
        edge_color='#909090',
        font_color='w',
        with_labels=True,
    )

    # Get edge labels
    edge_labels = nx.get_edge_attributes(graph, 'shared_variables')

    # Draw each edge label individually with its own color
    for edge, label in edge_labels.items():
        nx.draw_networkx_edge_labels(
            graph,
            pos,
            edge_labels={edge: label},
            # font_color=label_to_color(label)
        )


    plt.axis('off')
    plt.show()



if __name__ == "__main__":

    file_path = '../../samples/is_core/1.txt'

    with open(file_path, 'r') as file:
        file_content = file.read()

    inst = parse_bit_matrix(file_content)

    visualize_graph_by_clauses(inst)

