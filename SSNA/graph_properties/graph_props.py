import numpy as np
import networkx as nx
from networkx.algorithms import bipartite
import Queue 

# helper for is_balanced() 
def constrained_bfs(graph_obj, marker_map, marker, weight, start):
	#traverse only through edges having weight = 'weight'
	q = Queue.Queue()
	q.put(start)
	marker_map[start] = marker

	while not q.empty():
		cur_node = q.get()
		for adj_node in graph_obj.neighbors(cur_node):
			if adj_node not in marker_map and graph_obj[cur_node][adj_node]['weight'] == weight:
				q.put(adj_node)
				marker_map[adj_node] = marker

# check if a graph is balanced
def is_balanced(graph_obj, meta_data = False):
	undirected_graph_obj = nx.Graph(graph_obj)
	nodes = undirected_graph_obj.nodes()

	node_labels = {}
	cur_label = 0
	for node in nodes:
		if node not in node_labels:
			constrained_bfs(undirected_graph_obj, node_labels, cur_label, 1, node)
			cur_label += 1


	num_labels = cur_label

	set_graph = nx.Graph()
	set_graph.add_nodes_from([x for x in range(num_labels)])

	# check for mutual antagonism between sets and mutual friendship inside sets
	edges = undirected_graph_obj.edges()
	balanced = True
	for edge in edges:
		f = edge[0]
		s = edge[1]
		if undirected_graph_obj[f][s]['weight'] == 1:
			if node_labels[f] != node_labels[s]:	#this shouldn't happen
				balanced = False
				break
		if undirected_graph_obj[f][s]['weight'] == -1:
			set_graph.add_edge(node_labels[f], node_labels[s]);
			if node_labels[f] == node_labels[s]:
				balanced = False
				break

	metas = None
	if meta_data and balanced:
		# determine strength of balance (bipartite condition for sets antagonism)
		strong = None
		if bipartite.is_bipartite(set_graph):
			strong = True
		else:
			strong = False

		#sets
		sets = [[] for i in range(num_labels)]
		for node in node_labels:
			sets[node_labels[node]].append(node)

		#possible split
		split = None
		if strong:
			coloring = bipartite.color(set_graph)
			X = []
			Y = []
			for set_ in coloring:
				if coloring[set_] == 0:
					for node in sets[set_]:
						X.append(node)
				else:
					for node in sets[set_]:
						Y.append(node)
			split = (X, Y)

		metas = {}
		metas['num_original_sets'] = num_labels

		metas['original_sets'] = sets
		metas['strength'] = 'strong' if strong else 'weak'
		metas['possible_split'] = split

	return (balanced, metas)

'''
# sample
G = nx.Graph()

G.add_edge(1, 2, weight = 1)
G.add_edge(1, 4, weight = -1)
G.add_edge(3, 4, weight = -1)
G.add_edge(5, 6, weight = 1)
G.add_edge(1, 3, weight = -1)	#add/remove this to find the difference

print is_balanced(G, meta_data = True)
'''