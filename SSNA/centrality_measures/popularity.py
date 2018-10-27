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
    raise NotImplementedError
