import networkx as nx
import numpy as np
import scipy.sparse as ssp


def get_adjacency_matrix(graph_obj, meta_data=False):
    """
    This function returns a n x n adjacency matrix given a networkx graph object.

    Arguments:
        graph_obj : Networkx graph object
        meta_data : Argument to toggle to get meta_data of graph optionally. Default=False

    Returns:
        If meta_data is True, then a 2-tuple : (adjacency matrix, meta-data dictionary)
        If meta_data is False, then a 2-tuple : (adjacency matrix, None)
        Please note adjacency matrix returned is in sparse format. Use `.todense()` to convert
        to dense format
    """
    adj_mat = nx.adjacency_matrix(graph_obj)  # this is a sparse matrix
    metas = None
    if meta_data:
        metas = {}
        metas['density'] = adj_mat.getnnz() / (adj_mat.shape[0] * adj_mat.shape[1])
        metas['positive'] = (adj_mat > 0).getnnz()
        metas['negative'] = (adj_mat < 0).getnnz()
        metas['links'] = adj_mat.getnnz()
        metas['average_links'] = adj_mat.getnnz() / adj_mat.shape[0]
    return (adj_mat, metas)


def get_absolute_adjacency_matrix(graph_obj):
    """
    This function returns a n x n adjacency matrix given a networkx graph object, where the
    entries are absolute values of the weights between the edges

    Arguments:
        graph_obj : Networkx graph object

    Returns:
        n x n absolute adjacency matrix (sparse)
    """
    adj_mat, _ = get_adjacency_matrix(graph_obj, False)
    adj_mat = abs(adj_mat)
    return adj_mat


def get_symmetric_adjacency_matrix(graph_obj):
    """
    This function returns a n x n given a networkx graph object, which is the sum of the
    adjacency matrix and its transpose. This provides symmetry.

    Arguments:
        graph_obj : Networkx graph object

    Returns:
        n x n matrix (sparse)
    """
    adj_mat, _ = get_adjacency_matrix(graph_obj, False)
    adj_mat_t = adj_mat.transpose()
    return adj_mat + adj_mat_t


def get_absolute_symmetric_adjacency_matrix(graph_obj):
    """
    This function returns a n x n given a networkx graph object, which is the sum of the
    absolute adjacency matrix and its transpose. This provides symmetry.

    Arguments:
        graph_obj : Networkx graph object

    Returns:
        n x n matrix (sparse)
    """
    abs_adj_mat = get_absolute_adjacency_matrix(graph_obj)
    abs_adj_mat_t = abs_adj_mat.transpose()
    return abs_adj_mat + abs_adj_mat_t


def get_absolute_diagonal_degree_matrix(graph_obj):
    """
    This function returns a diagonal matrix D which is the defined as
    Dii = sum |Aij| for all j

    Arguments:
        graph_obj : Networkx graph object

    Returns:
        n x n matrix (sparse)
    """
    abs_adj_mat = get_absolute_adjacency_matrix(graph_obj)
    diag_entries = np.array(abs_adj_mat.sum(axis=1)).reshape(-1)
    return ssp.coo_matrix(np.diag(diag_entries))


def get_absolute_symmetric_diagonal_degree_matrix(graph_obj):
    """
    This function returns a diagonal matrix E which is the defined as
    Eii = sum |Bij| for all j

    Arguments:
        graph_obj : Networkx graph object

    Returns:
        n x n matrix (sparse)
    """
    abs_sym_adj_mat = get_absolute_symmetric_adjacency_matrix(graph_obj)
    diag_entries = np.array(abs_sym_adj_mat.sum(axis=1)).reshape(-1)
    return ssp.coo_matrix(np.diag(diag_entries))
