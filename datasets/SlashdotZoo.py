from subprocess import call
from utils import download_file

import os
import errno
import pandas as pd
import networkx as nx

class SlashdotZoo(object):
    """
    Class wrapping the Slashdot Zoo signed social network dataset.

    Arguments:
        root : Root folder to save the raw and processed datasets.
               Default: current directory ('.')
    """

    raw = "Slashdot-Zoo/raw"
    processed = "Slashdot-Zoo/processed"
    url = "http://konect.cc/files/download.tsv.slashdot-zoo.tar.bz2"
    pickle_name = "slashdot-zoo.gpickle"

    def __init__(self, root='.'):
        self.root = root
        self.raw_path = os.path.join(self.root, self.raw)
        self.proc_path = os.path.join(self.root, self.processed)

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
            x = len(df)

            # Format of each row: SOURCE, TARGET, SIGN.
            # Convert DataFrame to a list of tuples.
            tuples = [tuple(x) for x in df.values]

            print("- Pre-processing done.")

            # Build a directed graph.
            G = nx.DiGraph()
            G.add_weighted_edges_from(tuples)
            print("- Networkx graph created, saving...")

            if x != G.number_of_edges():
                raise ValueError("Error in parsing.")

            nx.write_gpickle(G, os.path.join(self.proc_path, self.pickle_name))
            print("- Graph saved.")

    @property
    def graph(self):
        return nx.read_gpickle(os.path.join(self.proc_path, self.pickle_name))
