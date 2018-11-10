# Link Prediction for Signed Networks

+ We have two classes of algorithms: baseline and algebraic similarity methods to predict the parity of the edge between two nodes in a directed signed graph.

### Baseline
+ These methods are based on intuition and normal graph theoretic concepts:
  + *Majority based voting* : From the graph given to us, we find the most frequently occuring sign and predict it. This is an uninformative algorithm.
  + *Symmetric prediction* : Given a graph, we find the symmetric (undirected) version of it, and predict the link in the results adjacency matrix. If neither link is present then we resort to majority based voting, and provide a default link to predict.
  + *Transitive prediction* : Given a signed graph, we find the square of the adjacency matrix. This will hence take into account the multiplicative transitivity, and provide a prediction based on this.

### Algebraic Similarity
+ These methods are based on some graph theoretic concepts as well as dimensionality reduction techniques:
  + *Adjacency Dimensionality Reduction* : We obtain the singular value decomposition (SVD) of the adjacency matrix until a rank `k`. We reconstruct the matrix and find the sign of the value at the reconstructed location, which is our prediction.
  + *Symmetric Adjacency Dimensionality Reduction* : We leverage the spectral theorem for symmetric matrices and perform the eigen-decomposition instead of SVD, which is faster than SVD.
  + *Exponential (Symmetric) Adjacency Dimensionality Reduction* : This is an extension of the Transitive prediction method wherein we take an infinite power series as the exponential function. Here too, we consider the dimensionality reduction of the resulting matrix for prediction.
