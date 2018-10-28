from ..graph_properties import get_adjacency_matrix

import networkx as nx

def uninformative_prediction(G, required_links):
    """
    Function to predict links in an uninformative manner, i.e., the majority
    parity. So, if there are more positive links that negative links, then a
    positive link is predicted and vice-versa

    Args:
        G : Graph to consider as training data
        required_links : List of tuples (a, b) where (a, b) denotes the outgoing
                         edge from `a` to `b`.

    Returns:
        List of {+1, -1} based on the properties of the graph
    """
    edges_weights = list(nx.get_edge_attributes(G, 'weight').values())
    edges_parity = [1 if w > 0 else -1 for w in edges_weights]
    if sum(edges_parity) > 0:
        return [1 for _ in required_links]
    else:
        return [-1 for _ in required_links]

def undirected_prediction(G, required_links, default=None):
    """
    Function to predict links in an undirected manner, i.e., if we have to
    predict a link for (a, b), we check if (b, a) exists. If yes, then we predict
    the same kind of link, else a default link.

    Args:
        G : Graph to consider as training data
        required_links : List of tuples (a, b) where (a, b) denotes the outgoing
                         edge from `a` to `b`.
        default : Values from 'positive', 'negative', None. If 'positive', then the
                  default link is +1, and if 'negative', then the default link is -1.
                  If None, then the default link is considered as the majority.

    Returns:
        List of {+1, -1} based on the properties of the graph
    """
    if default is None:
        edges_majority = sum(list(nx.get_edge_attributes(G, 'weight').values()))

    preds = []
    for pair in required_links:
        if G.has_edge(pair[1], pair[0]):
            if G[pair[1]][pair[0]]['weight'] > 0:
                preds.append(1)
            else:
                preds.append(0)
        else:
            if default is None:
                if edges_majority > 0:
                    preds.append(1)
                else:
                    preds.append(-1)
            elif default == 'positive':
                preds.append(1)
            elif default == 'negative':
                preds.append(-1)
            else:
                raise ValueError("Invalid argument for default") 
    return preds

def mult_trans_prediction(G, required_links, default=None):
    """
    Function to predict links using squared adjacency matrix and multiplicative
    transitivity property. The predictions for link from i to j is merely the i,j th
    entry of the squared adjacency matrix

    Args:
        G : Graph to consider as training data
        required_links : List of tuples (a, b) where (a, b) denotes the outgoing
                         edge from `a` to `b`.
        default : Values from 'positive', 'negative', None. If 'positive', then the
                  default link is +1, and if 'negative', then the default link is -1.
                  If None, then the default link is considered as the majority.

    Returns:
        List of {+1, -1} based on the properties of the graph
    """
    if default is None:
        edges_majority = sum(list(nx.get_edge_attributes(G, 'weight').values()))

    preds = []
    A = get_adjacency_matrix(G)
    sq_A = A * A
    for pair in required_links:
        if sq_A[pair[0], pair[1]] == 0:
            if default is None:
                if edges_majority > 0:
                    preds.append(1)
                else:
                    preds.append(-1)
            elif default == 'positive':
                preds.append(1)
            elif default == 'negative':
                preds.append(-1)
            else:
                raise ValueError("Invalid argument for default") 
        else:
            preds.append(sq_A[pair[0], pair[1]])
    return preds
