
import pandas as pd
import networkx as nx
import pickle

# Import dataset as a Pandas DataFrame.
df = pd.read_table("wiki-RfA.txt.gz", compression='gzip', sep='\n', header=None)
sequence = df[0].tolist()
print("-- Extracted and imported datset.")

# Isolate SOURCE, TARGET, VOTE.
src = []
tgt = []
vot = []
for index, element in enumerate(sequence):
    if index % 7 == 0:
        src.append(element[4:])
    elif index % 7 == 1:
        tgt.append(element[4:])
    elif index % 7 == 2:
        vot.append(int(element[4:]))
print("-- Attributes isolated.")

# Create hashmap for individuals across both SOURCE and TARGET.
src_set = set(src)
tgt_set = set(tgt)
hashmap = src.copy()
for element in tgt_set:
    if not element in src_set:
        hashmap.append(element)
src_set = set(hashmap)
hashmap = list(src_set)
print("-- Created hashmap for usernames.")

# Eliminate empty users and '0' links as we add to final list.
tuples = []
for index, sr in enumerate(src):
    if sr == '':
        continue
    elif vot[index] == 0:
        continue
    s = hashmap.index(sr)
    t = hashmap.index(tgt[index])
    v = vot[index]
    elem = (s, t, v)
    tuples.append(elem)
x = len(tuples)
print("-- Built tuple list, after eliminating empty users and edges.")

# Build a directed graph.
G = nx.DiGraph()
G.add_weighted_edges_from(tuples)
print("-- Built graph object.")

nx.write_gpickle(G, "../pickles/wiki-RfA.gpickle")
print("-- Graph Extracted and Pickled.")
