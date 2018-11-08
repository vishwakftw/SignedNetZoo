from subprocess import call
from .utils import download_file

import os
import errno
import random
import pandas as pd
import networkx as nx


class SlashdotZoo(object):
    """
    Class wrapping the Slashdot Zoo signed social network dataset.

    Arguments:
        root : Root folder to save the raw and processed datasets.
               Default: current directory ('.')
        split : Specify a number between 0 and 1. If `split` is not None, then two graphs are
                created for train and test.`split` * number of edges are considered for
                the training dataset, and (1 - `split`) * number of edges are considered
                for the testing dataset. Default : None
    """

    raw = "Slashdot-Zoo/raw"
    processed = "Slashdot-Zoo/processed"
    url = "http://konect.cc/files/download.tsv.slashdot-zoo.tar.bz2"
    pickle_name = "slashdot-zoo.gpickle"

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

        if os.path.isfile(os.path.join(self.proc_path, self.pickle_name)):
            print("- Graph ready.")
        else:
            print("- Pre-processing...")
            # Import dataset as a Pandas DataFrame, check edge count.
            call(['tar', 'xvjf', os.path.join(self.raw_path, os.path.basename(self.url)), '-C', self.raw_path])
            df = pd.read_table(os.path.join(self.raw_path, 'slashdot-zoo/out.matrix'),
                               sep=' ', skiprows=(0, 1), header=None)

            # Format of each row: SOURCE, TARGET, SIGN.
            # Convert DataFrame to a list of tuples.
            tuples = [tuple(x) for x in df.values]
            node_set = set()
            for tpl in tuples:
                node_set.update(tpl[:2])

            print("- Pre-processing done.")

            if self.split is None:
                print("- split is None, building one graph...")

                self._get_graph_impl(tuples, node_set)

                print("- Graph saved.")

            else:
                print("- split is {}, building two graphs...".format(self.split))

                random.shuffle(tuples)
                train_len = int(self.split * len(tuples))

                self._get_graph_impl(tuples[: train_len], node_set, suffix='train')
                self._get_graph_impl(tuples[train_len:], node_set, suffix='test')

                print("- Both Graphs saved.")

    def _get_graph_impl(self, tuples, node_set, suffix=''):
        # Build a directed graph.
        G = nx.DiGraph()
        G.add_nodes_from(node_set)
        G.add_weighted_edges_from(tuples)
        suffix = '.' + suffix

        nx.write_gpickle(G, os.path.join(self.proc_path, self.pickle_name + suffix))

    @property
    def graph(self):
        if self.split is None:
            return nx.read_gpickle(os.path.join(self.proc_path, self.pickle_name))

        else:
            return (nx.read_gpickle(os.path.join(self.proc_path, self.pickle_name + '.train')),
                    nx.read_gpickle(os.path.join(self.proc_path, self.pickle_name + '.test')))
