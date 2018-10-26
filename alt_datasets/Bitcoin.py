from utils import download_file

import os
import errno
import pandas as pd
import networkx as nx


class Bitcoin(object):
    """
    Class wrapping the Bitcoin OTC Trust Weighted Signed Network.

    Arguments:
        root : Root folder to save the raw and processed datasets.
               Default: current directory ('.')

    """

    raw = "Bitcoin-OTC-Trust-Network/raw"
    processed = "Bitcoin-OTC-Trust-Network/processed"
    url = "https://snap.stanford.edu/data/soc-sign-bitcoinotc.csv.gz"
    pickle_name = "soc-sign-bitcoinotc.gpickle"

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
            df = pd.read_table(os.path.join(self.raw_path, os.path.basename(self.url)),
                               compression='gzip', sep=',', header=None)
            x = len(df)

            # Format of each row: SOURCE, TARGET, RATING, TIME.
            # Removing the TIME column.
            del df[3]

            # Convert DataFrame to a list of tuples.
            tuples = [tuple(x) for x in df.values]

            print("- Pre-processing done.")

            # Build a directed graph.
            G = nx.DiGraph()
            G.add_weighted_edges_from(tuples)

            if x != G.number_of_edges():
                raise ValueError("Error in parsing.")

            nx.write_gpickle(G, os.path.join(self.proc_path, self.pickle_name))
            print("- Graph saved.")

    @property
    def graph(self):
        return nx.read_gpickle(os.path.join(self.proc_path, self.pickle_name))
