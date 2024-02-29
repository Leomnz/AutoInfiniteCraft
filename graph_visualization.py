import os
from datetime import datetime

import networkx as nx
import matplotlib.pyplot as plt

graph = nx.DiGraph()


def add_element(element):
    if element.parent1 is None and element.parent2 is None:
        graph.add_node(element.name, emoji=element.emoji, first_discovery=element.first_discovery)
    else:
        graph.add_node(element.name, emoji=element.emoji, first_discovery=element.first_discovery)
        graph.add_edges_from([(element.parent1, element.name), (element.parent2, element.name)])


def draw_graph():
    nx.draw(graph, with_labels=True)
    plt.show()
    print(list(graph.nodes(data=True)))


def save_graph():
    if not os.path.exists('Graphs'):
        os.makedirs('Graphs')
    # Save graph to file in /Graphs, name of graph should be date and time
    nx.write_gml(graph, f'Graphs/{datetime.now().strftime("%Y-%m-%d %H-%M-%S")}.gml')
