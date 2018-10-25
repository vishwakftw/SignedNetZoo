
import pandas as pd
import networkx as nx
import pickle
import hashlib

df = pd.read_table("wiki-RfA.txt.gz", compression='gzip', sep='\n', header=None)

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
