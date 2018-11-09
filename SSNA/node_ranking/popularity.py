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
    adj_mat = get_adjacency_matrix(G).tocsr()
    for i, j in zip(*adj_mat.nonzero()):
        adj_mat[i, j] = 1 if adj_mat[i, j] > 0 else -1
    return adj_mat.sum(axis=1)
