from ..graph_properties import get_adjacency_matrix, get_symmetric_adjacency_matrix

import scipy.sparse.linalg as sspl

def adjacency_dim_reduce(G, dim, required_links):
    """
    Function to get predictions for the parity of a link via dimensionality
    reduction techniques on the adjacency matrix.
    The link between u and v is predicted as follows:
        A = U S V^{T} => A_{dim} = U_{dim} S_{dim} V^{T}_{dim}.
    link(u, v) = sign(A_{dim}[u, v])

    Args:
        G : Graph to consider as training data
        dim : Dimensionality to reduce the adjacency matrix to.
              If dim > rank of adjacency matrix, then error out.
        required_links : List of tuples (a, b) where (a, b) denotes the outgoing
                         edge from `a` to `b`.

    Returns:
        List of {+1, -1} based on the properties of the graph
    """
    A = get_adjacency_matrix(G)
    u, s, v = sspl.svds(A, k=dim)
    u = u.transpose()
    preds = []
    for pair in required_links:
        i, j = pair
        entry_val = sum([s[k] * u[k][i] * v[k][j] for k in range(dim)])
        if entry_val >= 0:
            preds.append(1)
        else:
            preds.append(-1)
    return preds

def symmetric_adjacency_dim_reduce(G, dim, required_links):
    """
    Function to get predictions for the parity of a link via dimensionality
    reduction techniques on the symmetric adjacency matrix.
    The link between u and v is predicted as follows:
        A = U S U^{T} => A_{dim} = U_{dim} S_{dim} U^{T}_{dim}.
    link(u, v) = sign(A_{dim}[u, v])

    Args:
        G : Graph to consider as training data
        dim : Dimensionality to reduce the adjacency matrix to.
              If dim > rank of adjacency matrix, then error out.
        required_links : List of tuples (a, b) where (a, b) denotes the outgoing
                         edge from `a` to `b`.

    Returns:
        List of {+1, -1} based on the properties of the graph
    """
    A = get_symmetric_adjacency_matrix(G)
    w, v = sspl.eigsh(A, k=dim)
    v = v.transpose()
    preds = []
    for pair in required_links:
        i, j = pair
        entry_val = sum([s[k] * v[k][i] * v[k][j] for k in range(dim)])
        if entry_val >= 0:
            preds.append(1)
        else:
            preds.append(-1)
    return preds
