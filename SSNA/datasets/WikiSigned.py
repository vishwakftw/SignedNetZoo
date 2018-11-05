from .utils import download_file

import os
import errno
import random
import pandas as pd
import networkx as nx


class WikiSigned(object):
    """
    Class wrapping the WikiSigned social network dataset.

    Arguments:
        root : Root folder to save the raw and processed datasets.
               Default: current directory ('.')
        split : Specify a number between 0 and 1. If `split` is not None, then two graphs are
                created for train and test.`split` * number of edges are considered for
                the training dataset, and (1 - `split`) * number of edges are considered
                for the testing dataset. Default : None
    """

    raw = "WikiSigned-Social-Network/raw"
    processed = "WikiSigned-Social-Network/processed"
    url = "https://dl6.volafile.org/download/BlL3fT_CZ9F_m/WikiSigned.tsv"
    pickle_name = "wiki-signed.gpickle"

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
            df = pd.read_table(os.path.join(self.raw_path, os.path.basename(self.url)),
                               sep='\t', index_col=False, header=None)

            # Format of each row: SOURCE<space>TARGET, SIGN.
            # Convert DataFrame to a list of tuples.
            data = df.values
            tuples = []
            for edge in data:
                src, tgt = map(int, edge[0].split())
                val = edge[1]
                tuples.append((src, tgt, val))

            print("- Pre-processing done.")

            if self.split is None:
                print("- split is None, building one graph...")

                self._get_graph_impl(tuples)

                print("- Graph saved.")

            else:
                print("- split is {}, building two graphs...".format(self.split))

                random.shuffle(tuples)
                train_len = int(self.split * len(tuples))

                self._get_graph_impl(tuples[: train_len], suffix='train')
                self._get_graph_impl(tuples[train_len:], suffix='test')

                print("- Both Graphs saved.")

    def _get_graph_impl(self, tuples, suffix=''):
        # Build a directed graph.
        G = nx.DiGraph()
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