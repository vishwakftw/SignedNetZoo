from .utils import download_file, get_node_set_map

import os
import errno
import random
import pandas as pd
import networkx as nx


class Twitter(object):
    """
    Class wrapping the Sentiment140 - Twitter dataset.

    Arguments:
        root : Root folder to save the raw and processed datasets.
               Default: current directory ('.')
        split : Specify a number between 0 and 1. If `split` is not None, then two graphs are
                created for train and test.`split` * number of edges are considered for
                the training dataset, and (1 - `split`) * number of edges are considered
                for the testing dataset. Default : None
    """

    raw = "Twitter-Sentiment140/raw"
    processed = "Twitter-Sentiment140/processed"
    url = "https://www.kaggle.com/kazanova/sentiment140/downloads/sentiment140.zip"
    pickle_name = "tweets-s140.gpickle"

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
            # Import dataset as a Pandas DataFrame.
            df = pd.read_table(os.path.join(self.raw_path, os.path.basename(self.url)),
                               delimiter=',', encoding='latin-1', compression='zip', header=None)

            biased_dataframe = base_dataframe.loc[df[0] != 2]

            tweets = biased_dataframe[5].values
            uni = []
            multi = []
            for tweet in tweets:
                words = tweet.split()
                uniflag = False
                multiflag = False
                for word in words:
                    if word[0] == '@' and len(word) > 1 and not uniflag:
                        uniflag = True
                    elif word[0] == '@' and len(word) > 1 and uniflag:
                        multiflag = True
                if multiflag:
                    multi.append(tweet)
                elif uniflag:
                    uni.append(tweet)

            src_list = biased_dataframe[4].values
            tweet_list = biased_dataframe[5].values
            sentiment_list = biased_dataframe[0].values
            uni_list = []
            multi_list = []

            for index, tweet in enumerate(tweet_list):
                target = []
                words = tweet.split()
                uniflag = False
                target = ''
                targets = []
                for word in words:
                    if word[0] == '@' and len(word) > 1 and not uniflag:
                        target = word[1:]
                        uniflag = True
                    elif word[0] == '@' and len(word) > 1 and uniflag:
                        targets.append(word[1:])
                if len(targets) != 0:
                    targets.append(target)
                    multi_list.append([src_list[index], targets, sentiment_list[index]])
                elif uniflag:
                    uni_list.append([src_list[index], target, sentiment_list[index]])

            src_users = [x[0] for x in uni_list]
            tgt_users = [x[1] for x in uni_list]
            src_users_set = set(src_users)
            tgt_users_set = set(tgt_users)
            intersection = src_users_set.intersection(tgt_users_set)

            user_cluster = src_users_set.union(tgt_users_set)
            user_list = list(user_cluster)
            hashmap = {user:index for index, user in enumerate(user_list)}

            init_tuples = []
            for row in uni_list:
                if row[2] == 0:
                    v = -1
                elif row[2] == 4:
                    v = 1
                s, t = hashmap[row[0]], hashmap[row[1]]
                init_tuples.append((s, t, v))

            edges = [(x,y) for (x,y,z) in init_tuples]
            distinct_edges = set(edges)

            init_tuples.sort(key=lambda x: x[0]*1000000 + x[1])
            tuples = []
            prev_edge = init_tuples[0]
            average_flag = False
            average_set = []
            for i in range(1, len(init_tuples)):
                curr_edge = init_tuples[i]
                if not edges_are_same(curr_edge, prev_edge) and not average_flag:
                    tuples.append(prev_edge)
                elif edges_are_same(curr_edge, prev_edge) and not average_flag:
                    average_set.append(prev_edge)
                    average_flag = True
                elif edges_are_same(curr_edge, prev_edge) and average_flag:
                    average_set.append(prev_edge)
                elif not edges_are_same(curr_edge, prev_edge) and average_flag:
                    average_set.append(prev_edge)
                    equivalent_edge, valid = get_equivalent_edge(average_set)
                    average_flag = False
                    average_set = []
                    if valid:
                        tuples.append(equivalent_edge)
                prev_edge = curr_edge
            if average_flag:
                average_set.append(prev_edge)
                equivalent_edge, valid = get_equivalent_edge(average_set)
                if valid:
                    tuples.append(equivalent_edge)
            else:
                tuples.append(prev_edge)


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

                self._get_graph_impl(tuples[: train_len], node_map.values(), suffix='train')
                self._get_graph_impl(tuples[train_len:], node_map.values(), suffix='test')

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
            return (nx.read_gpickle(os.path.join(self.proc_path, self.pickle_name + '.train')),
                    nx.read_gpickle(os.path.join(self.proc_path, self.pickle_name + '.test')))
