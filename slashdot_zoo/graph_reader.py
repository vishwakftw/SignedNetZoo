import networkx as nx
from argparse import ArgumentParser

def _lines_in_file(filename):
    with open(filename) as f:
        for i, _ in enumerate(f):
            pass
    return i + 1

def graph_reader(filename):
    graph_data = []
    with open(filename) as f:
        for i, line in enumerate(f):
            vals = line.split(' ')
            if len(vals) == 4:
                vals = vals[:-1]
            elif len(vals) == 3:
                vals[-1] = vals[-1][:-1]
            else:
                raise ValueError("Incorrect format in line {}".format(i + 1))
            vals = [int(v) for v in vals]
            graph_data.append(tuple(vals))

    assert len(graph_data) == _lines_in_file(p.graph_file),
           "Incorrect file read - input file has {} lines "
           "while only {} edges have been added".format(_lines_in_file(p.graph_file), len(graph_data))

    G = nx.DiGraph()  # directed graph
    G.add_weighted_edges_from(graph_data)

    return G

if __name__ == '__main__':
    p = ArgumentParser()
    p.add_argument('--graph_file', type=str, required=True
                               help='File location to get graph in trivial graph format\
                                     <node1>[space]<node2>[space]<weight>')
    p = p.parse_args()

    G = graph_reader(p.graph_file)