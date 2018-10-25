
import pandas as pd
import networkx as nx
import pickle


# Import dataset as a Pandas DataFrame.
df = pd.read_table("wiki-RfA.txt.gz", compression='gzip', sep='\n', header=None)
sequence = df[0].tolist() # len(sequence) = 1387925
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
# len(src/tgt/vot) = 198275


# Create hashmap for individuals across both SOURCE and TARGET.
src_set = set(src) # len(src_set) = 10417
tgt_set = set(tgt) # len(tgt_set) = 3497
# tgt_set < src_set = False
# len(tgt_set.intersection(src_set)) = 2533
hashmap = list(src_set)
for element in tgt_set:
    if not element in src_set:
        hashmap.append(element)
# len(hashmap) = 11381
# tgt_set < set(hashmap) = True
print("-- Created hashmap for usernames.")


# Eliminate empty users and '0' links as we add to final list.
tuples = []
for index, source in enumerate(src):
    if source == '':
        continue
    elif vot[index] == 0:
        continue
    s = hashmap.index(source)
    t = hashmap.index(tgt[index])
    v = vot[index]
    elem = (s, t, v)
    tuples.append(elem)
print("-- Built tuple list, after eliminating empty users and edges.")

# Build a directed graph.
G = nx.DiGraph()
G.add_weighted_edges_from(tuples)
print("-- Built graph object.")

nx.write_gpickle(G, "../pickles/wiki-RfA.gpickle")
print("-- Graph Extracted and Pickled.")
