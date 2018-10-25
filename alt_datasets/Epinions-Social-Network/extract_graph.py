import pandas as pd
import networkx as nx
import pickle

# Import dataset as a Pandas DataFrame, check edge count.
df = pd.read_table("soc-sign-epinions.txt.gz", compression='gzip', sep='\t', skiprows=(0,1,2,3), header=None)
x = len(df)
print("-- Extracted and imported dataset.")

# Format of each row: SOURCE, TARGET, SIGN.

# Convert DataFrame to a list of tuples.
tuples = [tuple(x) for x in df.values]
print("-- Attributes isolated and built tuple list.")

# Build a directed graph.
G = nx.DiGraph()
G.add_weighted_edges_from(tuples)
print("-- Built graph object.")

# Confirm graph integrity.
if x == G.number_of_edges():
    print("-- Graph Integrity Maintained.")
    # Pickling Graph Object
    nx.write_gpickle(G, "../pickles/soc-sign-epinions.gpickle")
    print("-- Graph Extracted and Pickled.")
else:
    print("-- Graph Integrity Lost.")
