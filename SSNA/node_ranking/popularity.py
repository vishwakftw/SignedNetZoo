import networkx as nx
from ..graph_properties import get_adjacency_matrix

def fans_minus_freaks(G):
    """
    Function to compute the fans-minus-freaks score for a signed graph

    Given a node `v` of a graph G, a fan of `v` are the neighbours of `v` connected via
    a positive weight. Similarly, a freak of `v` are the neighbours of `v` connected via
    a negative weight.

    Args:
        G : a signed social network graph

    Returns:
        A list containing the FMF score for each node of the graph
    """
    n = len(G.nodes)
    fmf_arr = [0]*n
    i = 0
    for (u,v,w) in G.edges.data('weight'):
        if(w > 0):
            fmf_arr[v-1] += 1
        elif(w < 0):
            fmf_arr[v-1] -= 1
    for a in fmf_arr:
        print(a)
    return fmf_arr


'''
# sample
G = nx.Graph()

G.add_edge(1, 2, weight = 1)
G.add_edge(1, 4, weight = -1)
G.add_edge(3, 4, weight = -1)
G.add_edge(5, 6, weight = 1)
G.add_edge(1, 3, weight = -1)   #add/remove this to find the difference

fans_minus_freaks(G)
'''