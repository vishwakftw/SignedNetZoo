try:
    import queue as Queue
except ImportError:
    import Queue


# helper for is_balanced()
def constrained_bfs(graph_obj, marker_map, marker, weight, start):
    # traverse only through edges having weight = 'weight'
    q = Queue.Queue()
    q.put(start)
    marker_map[start] = marker

    while not q.empty():
        cur_node = q.get()
        for adj_node in graph_obj.neighbors(cur_node):
            if adj_node not in marker_map and graph_obj[cur_node][adj_node]['weight'] == weight:
                q.put(adj_node)
                marker_map[adj_node] = marker
