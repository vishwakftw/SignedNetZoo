from .utils import download_file, get_node_set_map

import os
import errno
import random
import pandas as pd
import networkx as nx


class Wikipedia(object):
    """
    Class wrapping the Wikipedia Requests for Adminship dataset.

    Arguments:
        root : Root folder to save the raw and processed datasets.
               Default: current directory ('.')
        split : Specify a number between 0 and 1. If `split` is not None, then two graphs are
                created for train and test.`split` * number of edges are considered for
                the training dataset, and (1 - `split`) * number of edges are considered
                for the testing dataset. Default : None
    """

    raw = "Wikipedia-Requests-for-Adminship/raw"
    processed = "Wikipedia-Requests-for-Adminship/processed"
    url = "https://snap.stanford.edu/data/wiki-RfA.txt.gz"
    pickle_name = "wiki-RfA.gpickle"

    def __init__(self, root='.', split=None):
        self.root = root
        self.raw_path = os.path.join(self.root, self.raw)
        self.proc_path = os.path.join(self.root, self.processed)
        self.split = split
        if self.split is not None:
            assert 0 < self.split < 1, "split argument out of range"

        try:
            os.makedirs(self.raw_path)
            os.makedirs(self.proc_path)
        except OSError as e:
            if e.errno == errno.EEXIST:
                pass
            else:
                raise

        download_file(self.raw_path, self.url)
        self._get_graph()

    def _get_graph(self):
        print("- Obtaining Networkx Graph...")

        if self.split is None and os.path.isfile(os.path.join(self.proc_path, self.pickle_name)):
            print("- Graph ready.")
        elif self.split is not None and (os.path.isfile(os.path.join(self.proc_path,
                                                        self.pickle_name + '.train_{}'
                                                        .format(self.split))) or
                                         os.path.isfile(os.path.join(self.proc_path,
                                                        self.pickle_name + '.test_{}'.
                                                        format(1 - self.split)))):
            print("- Graphs ready.")
        else:
            print("- Pre-processing...")
            # Import dataset as a Pandas DataFrame.
            df = pd.read_table(os.path.join(self.raw_path, os.path.basename(self.url)),
                               compression='gzip', sep='\n', header=None)
            sequence = df[0].tolist()
            assert len(sequence) == 1387925, "Error in download."

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

            assert len(src) == len(tgt) == len(vot) == 198275, "Error in download."

            # Create hashmap for individuals across both SOURCE and TARGET.
            src_set, tgt_set = set(src), set(tgt)

            assert len(src_set) == 10417, "Error in parsing."
            assert len(tgt_set) == 3497, "Error in parsing."
            assert not tgt_set < src_set, "Error in parsing."

            hashmap = list(src_set | tgt_set)

            # Eliminate empty users and '0' links as we add to final list.
            tuples = []
            for index, source in enumerate(src):
                if source == '':
                    continue
                elif vot[index] == 0:
                    continue
                s, t, v = hashmap.index(source), hashmap.index(tgt[index]), vot[index]
                tuples.append((s, t, v))
            print("- Pre-processing done.")

            tuples, node_map = get_node_set_map(tuples)

            if self.split is None:
                print("- split is None, building one graph...")

                self._get_graph_impl(tuples, node_map.values())

                print("- Graph saved.")

            else:
                print("- split is {}, building two graphs...".format(self.split))

                random.shuffle(tuples)
                train_len = int(self.split * len(tuples))

                self._get_graph_impl(tuples[: train_len], node_map.values(),
                                     suffix='train_{}'.format(self.split))
                self._get_graph_impl(tuples[train_len:], node_map.values(),
                                     suffix='test_{}'.format(1 - self.split))

                print("- Both Graphs saved.")

    def _get_graph_impl(self, tuples, node_set, suffix=''):
        # Build a directed graph.
        G = nx.DiGraph()
        G.add_nodes_from(node_set)
        G.add_weighted_edges_from(tuples)
        if suffix != '':
            suffix = '.' + suffix

        nx.write_gpickle(G, os.path.join(self.proc_path, self.pickle_name + suffix))

    @property
    def graph(self):
        if self.split is None:
            return nx.read_gpickle(os.path.join(self.proc_path, self.pickle_name))

        else:
            return (nx.read_gpickle(
                        os.path.join(self.proc_path,
                                     self.pickle_name + '.train_{}'.format(self.split))),
                    nx.read_gpickle(
                        os.path.join(self.proc_path,
                                     self.pickle_name + '.test_{}'.format(1 - self.split))))
