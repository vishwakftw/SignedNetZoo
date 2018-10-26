from utils import download_file

import os
import errno
import pandas as pd
import networkx as nx


class Epinions(object): 
    """
    Class wrapping the Epinions social network dataset.

    Arguments:
        root : Root folder to save the raw and processed datasets.
               Default: current directory ('.')
    """

    raw = "Epinions-Social-Network/raw"
    processed = "Epinions-Social-Network/processed"
    url = "https://snap.stanford.edu/data/soc-sign-epinions.txt.gz"
    pickle_name = "soc-sign-epinions.gpickle"

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
                               compression='gzip', sep='\t', skiprows=(0,1,2,3), header=None)
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
