from functools import partial
from argparse import ArgumentParser

import numpy as np
import SignedNetZoo as snz


def get_actual_edges(edgelist, graph):
    return [1 if graph[src][dst]['weight'] >= 0 else -1 for (src, dst) in edgelist]


def get_algorithm_from_string(string):
    map_string = {'majority': 'uninformative_prediction',
                  'undirected': 'undirected_prediction',
                  'transitive': 'mult_trans_prediction',
                  'transitive_radius': 'mult_trans_prediction_with_radius',
                 }
    if string in map_string.keys():
        return getattr(snz.link_prediction.baseline, map_string[string])
    elif string == 'adjacency_dim_reduce':
        return snz.link_prediction.algebraic_similarity.adjacency_dim_reduce
    elif string == 'sym_adjacency_dim_reduce':
        return snz.link_prediction.algebraic_similarity.symmetric_adjacency_dim_reduce
    elif string == 'exp_adjacency_dim_reduce' or string == 'exp_sym_adjacency_dim_reduce':
        return snz.link_prediction.algebraic_similarity.exponential_adjacency_dim_reduce


parser = ArgumentParser()
parser.add_argument('--datasetname', type=str, required=True,
                    choices=['Bitcoin', 'Epinions', 'SlashdotZoo',
                             'Twitter', 'WikiSigned', 'Wikipedia'],
                    help='Name of the dataset')
parser.add_argument('--dataroot', type=str, required=True, help='Location of the dataset')
parser.add_argument('--split_val', type=float, default=0.8, help='Split for train/test')
parser.add_argument('--algorithms', type=str, default=['majority'], nargs='+',
                    choices=['majority', 'undirected', 'transitive',
                             'adjacency_dim_reduce', 'sym_adjacency_dim_reduce',
                             'exp_adjacency_dim_reduce', 'exp_sym_adjacency_dim_reduce'],
                    help='Algorithm to use. If you specify more than one, they will all be run')
parser.add_argument('--dims', type=int, default=[5], nargs='+',
                    help='Rank for dimensionality reduction for algebraic similarity')
args = parser.parse_args()

dataset = getattr(snz.datasets, args.datasetname)(root=args.dataroot, split=args.split_val)

train, test = dataset.graph
testing_edges = list(test.edges())

actual_vals = np.array(get_actual_edges(testing_edges, test))
for algo in args.algorithms:
    pred_func = get_algorithm_from_string(algo)
    if 'dim_reduce' in algo:
        kwargs = {}
        if algo == 'exp_sym_adjacency_dim_reduce':
            kwargs['symmetric'] = True
        for dim in args.dims:
            kwargs['dim'] = dim
            pred_func = partial(pred_func, **kwargs)
            pred_vals = np.array(pred_func(G=train, required_links=testing_edges))
            print("Confusion matrix with {} and dim = {}\n{}"
                  .format(algo, dim,
                          snz.link_prediction.utils.confusion_matrix(actual_vals, pred_vals)))
    else:
        pred_vals = np.array(pred_func(G=train, required_links=testing_edges))
        print("Confusion matrix with {}\n{}"
              .format(algo, snz.link_prediction.utils.confusion_matrix(actual_vals, pred_vals)))
