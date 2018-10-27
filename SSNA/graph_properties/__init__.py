from .graph_defs import (get_adjacency_matrix, get_absolute_adjacency_matrix,
                         get_symmetric_adjacency_matrix, get_absolute_symmetric_adjacency_matrix,
                         get_absolute_diagonal_degree_matrix, get_absolute_symmetric_diagonal_degree_matrix)
from . import clustering_coeffs

# These are not required
del graph_defs
del clustering_coeffs.np, clustering_coeffs.gd
