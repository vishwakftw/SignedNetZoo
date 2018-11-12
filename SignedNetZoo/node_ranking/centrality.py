from ..graph_properties import get_adjacency_matrix


def pagerank(G, signed=True, symmetric=False, alpha=0.8, max_iter=100):
    """
    Function to get the PageRank centrality scores for each node in a signed network.

    Arguments:
        G : graph to compute PageRank on
        signed : Consider a signed network. Default: True
        symmetric : Consider a symmetric network. Default: False
        alpha : teleportation parameter for PageRank to cover for dangling edges.
                Default: 0.8
        max_iter : maximum number of iterations to perform the power iteration to obtain
                   an approximation of the steady state vector
                   Default: 100

    Returns:
        A dictionary with keys as nodes and values as PageRank values
    """
    from networkx import link_analysis

    # By default, the graph is assumed to be signed and asymmetric
    if not signed:
        for u, v, d in G.edges(data=True):
            G[u][v]['weight'] = abs(G[u][v]['weight'])
    if symmetric:
        nodes = list(G.nodes())
        for i in range(len(nodes)):
            for j in range(i, len(nodes)):
                if G.has_edge(nodes[i], nodes[j]):
                    if G.has_edge(nodes[j], nodes[i]):
                        # This happens due to A + A.T
                        G[nodes[i]][nodes[j]]['weight'] += G[nodes[j]][nodes[i]]['weight']
                        G[nodes[j]][nodes[i]]['weight'] += G[nodes[i]][nodes[j]]['weight']
                    else:
                        G.add_edge(nodes[j], nodes[i], weight=G[nodes[i]][nodes[j]]['weight'])

    return link_analysis.pagerank_scipy(G, alpha=alpha, max_iter=max_iter)


def negativerank(G, beta, alpha=0.8, max_iter=100):
    """
    Function to get the Negative rank of a nodes in a graph.
    Negative rank is given by:
        Signed Spectral Rank - eta * Page Rank

    Arguments:
        G : graph to compute PageRank and its variants on
        beta : parameter for Negative Rank
        alpha : teleportation parameter for PageRank to cover for dangling edges.
                Default: 0.8
        max_iter : maximum number of iterations to perform the power iteration to obtain
                   an approximation of the steady state vector
                   Default: 100

    Returns:
        A dictionary with keys as nodes and values as PageRank values
    """
    # PageRank vals
    PR = pagerank(G, alpha=alpha, max_iter=max_iter)
    SR = pagerank(G, signed=True, alpha=alpha, max_iter=max_iter)
    NR = {}
    for key in SR.keys():
        NR[key] = SR[key] - beta * PR[key]
    return NR


def exponentialrank(G, mu=0.2, max_iter=100):
    """
    Function to get the ranking of nodes in a graph by Exponential Ranking,
    proposed by Traag et al, "Exponential Ranking: taking into account negative links"

    Arguments:
        G : graph to compute Exponential Rank
        mu : mu parameter in the algorithm. Default: 0.2
        max_iter : maximum number of iterations to perform the power iteration to obtain
                   an approximation of the steady state vector
                   Default: 100

    Returns:
        A dictionary with keys as nodes and values as PageRank values
    """
    from numpy import full, exp

    adj, _ = get_adjacency_matrix(G)
    adj = adj.T
    p = full(adj.shape[0], 1 / adj.shape[0])
    for i in range(max_iter):
        k = adj.dot(p)
        p = exp(k / mu)
        p = p / p.sum()
    final_vals = adj.dot(p)
    return {i: final_vals[i] for i in range(0, adj.shape[0])}
