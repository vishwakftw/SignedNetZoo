from . import graph_defs as gd


def clustering_coeff(graph_obj):
    abs_adj_mat = gd.get_absolute_adjacency_matrix(graph_obj)
    sq_abs_adj_mat = abs_adj_mat.dot(abs_adj_mat)
    return abs_adj_mat.multiply(sq_abs_adj_mat).sum() / sq_abs_adj_mat.sum()


def sign_clustering_coeff(graph_obj):
    adj_mat, _ = gd.get_adjacency_matrix(graph_obj)
    sq_adj_mat = adj_mat.dot(adj_mat)
    abs_adj_mat = abs(adj_mat)
    sq_abs_adj_mat = abs_adj_mat.dot(abs_adj_mat)
    return adj_mat.multiply(sq_adj_mat).sum() / sq_abs_adj_mat.sum()


def relative_sign_clustering_coeff(graph_obj):
    C = clustering_coeff(graph_obj)
    C_s = sign_clustering_coeff(graph_obj)
    return C_s / C
