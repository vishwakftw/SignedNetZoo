# Graph Properties
The current directory has a list of various functions pertaining to Signed Graphs / Social Networks.

### Graph Definitions
+ Usual graph definitions are included here. The functions included are:
  + *Adjancency matrix (with meta data)* : to get the adjacency matrix of a signed graph, in addition to optional metadata about the graph
  + *Absolute Adjacency matrix* : to get the absolute adjacency matrix of a signed graph. Here the entries are the absolute values of the entries in the original adjacency matrix
  + *Symmetric Adjacency Matrix* : Since we might be dealing with directed signed graphs, we convert the adjacency matrix to a symmetric version by adding the transpose of the original adjacency matrix to itself.
  + *Absolute Symmetric Adjacency Matrix* : to get the absolute version of the symmetric adjacency matrix as specified above in the case of the adjacency matrix.
  + *Absolute Diagonal Degree Matrix* : to get the out-degree of vertices in a directed signed graph.
  + *Absolute Symmetric Diagonal Degree Matrix* : to get the degree of the vertices in directed signed graph. This is computed using the absolute symmetric adjacency matrix

### Clustering Coefficients
+ Clustering Coefficients help us analyze the transitivity in a graph.
  + *Normal Clustering Coefficient* : we use the definition provided in **Collective dynamics of 'small-world' networks** by D J Watts and S H Strogatz.
  + *Signed Clustering Coefficient* : this is the extension of the normal clustering coefficients for signed graphs defined in **The Slashdot Zoo: Mining a Social Network with Negative Edges** by J. Kunegis _et al_.
  + *Relative Sign Clustering Coefficient* : this is the ratio of the signed clustering coefficient to the normal clustering coefficient. This helps us quantify the amount of multiplicative transitivity present in the graph.

### Balance
+ Balance is an older notion for finding multiplicative transitivity. We implement a function to check for balance using constrained breadth first search based on the definitions in **On the notion of balance of a signed graph** by Frank Harary and **Networks, Crowds, and Markets: Reasoning About a Highly Connected World** by David Easley and Jon Kleinberg.
