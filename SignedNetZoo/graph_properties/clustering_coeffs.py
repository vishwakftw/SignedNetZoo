from . import graph_defs as gd


def clustering_coeff(graph_obj):
    """
    Function to get clustering coefficient for a given graph.

    Args:
        graph_obj : NetworkX graph object

    Returns:
        float representing clustering coefficient of the graph.
    """
    abs_adj_mat = gd.get_absolute_adjacency_matrix(graph_obj)
    sq_abs_adj_mat = abs_adj_mat.dot(abs_adj_mat)
    return abs_adj_mat.multiply(sq_abs_adj_mat).sum() / sq_abs_adj_mat.sum()


def sign_clustering_coeff(graph_obj):
    """
    Function to get signed clustering coefficient for a given graph.

    Args:
        graph_obj : NetworkX graph object

    Returns:
        float representing signed clustering coefficient of the graph.
    """
    adj_mat, _ = gd.get_adjacency_matrix(graph_obj)
    sq_adj_mat = adj_mat.dot(adj_mat)
    abs_adj_mat = abs(adj_mat)
    sq_abs_adj_mat = abs_adj_mat.dot(abs_adj_mat)
    return adj_mat.multiply(sq_adj_mat).sum() / sq_abs_adj_mat.sum()


def relative_sign_clustering_coeff(graph_obj):
    """
    Function to get relative signed clustering coefficient for a given graph.
    This is defined as the ratio between the signed clustering coefficient and
    the clustering coefficient.

    Args:
        graph_obj : NetworkX graph object

    Returns:
        float representing relative signed clustering coefficient of the graph.
    """
    C = clustering_coeff(graph_obj)
    C_s = sign_clustering_coeff(graph_obj)
    return C_s / C
