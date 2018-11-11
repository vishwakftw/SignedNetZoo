from functools import partial
from argparse import ArgumentParser
from matplotlib import pyplot as plt

import numpy as np
import seaborn as sb
import SignedNetZoo as snz


def get_algorithm_from_string(string):
    if string == 'pagerank':
        return partial(snz.node_ranking.pagerank, signed=False)
    elif string == 'signed_pagerank':
        return partial(snz.node_ranking.pagerank, signed=True)
    elif string == 'sym_pagerank':
        return partial(snz.node_ranking.pagerank, symmetric=True, signed=False)
    elif string == 'exp_pagerank':
        return snz.node_ranking.exponentialrank


parser = ArgumentParser()
parser.add_argument('--datasetname', type=str, required=True,
                    choices=['Bitcoin', 'Epinions', 'SlashdotZoo',
                             'Twitter', 'WikiSigned', 'Wikipedia'],
                    help='Name of the dataset')
parser.add_argument('--dataroot', type=str, required=True, help='Location of the dataset')
parser.add_argument('--algorithms', type=str, default=['pagerank'], nargs='+',
                    choices=['pagerank', 'signed_pagerank', 'sym_pagerank', 'exp_pagerank'],
                    help='Algorithm to use. If you specify more than one, they will all be run')
args = parser.parse_args()

dataset = getattr(snz.datasets, args.datasetname)(root=args.dataroot)
graph = dataset.graph

n_subplots = '1{}1'.format(len(args.algorithms))
n_subplots = int(n_subplots)

for i, algo in enumerate(args.algorithms):
    plt.subplot(n_subplots + i)
    algo_vals = list(get_algorithm_from_string(algo)(graph).values())
    sb.kdeplot(np.array(algo_vals), shade=True)
    plt.xlabel('Reputation values')
    plt.ylabel('Density')
    plt.title(algo)

plt.suptitle('Distribution of reputation values'.format(algo))
plt.show()
