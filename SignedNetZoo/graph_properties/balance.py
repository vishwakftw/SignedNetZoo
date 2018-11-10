from .utils import constrained_bfs
from networkx.algorithms import bipartite

import networkx as nx


# check if a graph is balanced
def is_balanced(graph_obj, meta_data=False):
    """
    Function to check if a signed graph is balanced. The algorithm used here has been
    adopted from the paper "On the notion of balance of a signed graph" by Frank Harary
    and the boook "Networks, Crowds, and Markets: Reasoning About a Highly Connected World"
    by David Easley and Jon Kleinberg.

    Args:
        graph_obj : The signed graph to pass
        meta_data : Option to get meta data regarding the nature of the balance in the graphs.
                    Default: False

    Returns:
        A two tuple: (bool, meta-data dict). The meta-data dict is None, if meta_data is False
    """
    if graph_obj.is_directed():
        undirected_graph_obj = graph_obj.to_undirected()
    else:
        undirected_graph_obj = graph_obj

    nodes = undirected_graph_obj.nodes()

    node_labels = {}
    cur_label = 0
    for node in nodes:
        if node not in node_labels:
            constrained_bfs(undirected_graph_obj, node_labels, cur_label, 1, node)
            cur_label += 1

    num_labels = cur_label

    set_graph = nx.Graph()
    set_graph.add_nodes_from([x for x in range(num_labels)])

    # check for mutual antagonism between sets and mutual friendship inside sets
    edges = undirected_graph_obj.edges()
    balanced = True
    for edge in edges:
        f = edge[0]
        s = edge[1]
        if undirected_graph_obj[f][s]['weight'] == 1:
            if node_labels[f] != node_labels[s]:    # this shouldn't happen
                balanced = False
                break
        if undirected_graph_obj[f][s]['weight'] == -1:
            set_graph.add_edge(node_labels[f], node_labels[s])
            if node_labels[f] == node_labels[s]:
                balanced = False
                break

    metas = None
    if meta_data and balanced:
        # determine strength of balance (bipartite condition for sets antagonism)
        strong = None
        if bipartite.is_bipartite(set_graph):
            strong = True
        else:
            strong = False

        # sets
        sets = [[] for i in range(num_labels)]
        for node in node_labels:
            sets[node_labels[node]].append(node)

        # possible split
        split = None
        if strong:
            coloring = bipartite.color(set_graph)
            X = set()
            Y = set()
            for set_ in coloring:
                if coloring[set_] == 0:
                    for node in sets[set_]:
                        X.add(node)
                else:
                    for node in sets[set_]:
                        Y.add(node)
            split = {frozenset(X), frozenset(Y)}

        metas = {}
        metas['num_original_sets'] = num_labels

        metas['original_sets'] = sets
        metas['strength'] = 'strong' if strong else 'weak'
        metas['possible_split'] = split

    return (balanced, metas)
