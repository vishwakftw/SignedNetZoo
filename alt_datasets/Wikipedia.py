from utils import download_file

import os
import errno
import pandas as pd
import networkx as nx


class Wikipedia(object): 
    """
    Class wrapping the Wikipedia Requests for Adminship dataset.

    Arguments:
        root : Root folder to save the raw and processed datasets.
               Default: current directory ('.')
    """

    raw = "Wikipedia-Requests-for-Adminship/raw"
    processed = "Wikipedia-Requests-for-Adminship/processed"
    url = "https://snap.stanford.edu/data/wiki-RfA.txt.gz"
    pickle_name = "wiki-RfA.gpickle"

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

            # Build a directed graph.
            G = nx.DiGraph()
            G.add_weighted_edges_from(tuples)

            print("- Networkx graph created, saving...")
            nx.write_gpickle(G, os.path.join(self.proc_path, self.pickle_name))
            print("- Graph saved.")

    @property
    def graph(self):
        return nx.read_gpickle(os.path.join(self.proc_path, self.pickle_name))
