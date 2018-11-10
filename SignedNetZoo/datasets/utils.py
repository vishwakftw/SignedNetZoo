from tqdm import tqdm

try:
    import urllib.request
except ImportError:
    from six.moves import urllib
import os


def gen_bar_updater(pbar):
    """
    TQDM hook for progress bar during download
    """
    def bar_update(count, block_size, total_size):
        if pbar.total is None and total_size:
            pbar.total = total_size
        progress_bytes = count * block_size
        pbar.update(progress_bytes - pbar.n)

    return bar_update


def download_file(path, link):
    """
    Function to download a file from `link` and save to `path`.

    Args:
        path : path to the directory to save the file at
        link : URL for download
    """
    local_path = os.path.join(path, os.path.basename(link))
    if os.path.isfile(local_path):
        print("- File already downloaded.")
        return
    urllib.request.urlretrieve(link, local_path,
                               reporthook=gen_bar_updater(tqdm(unit='B', unit_scale=True)))


def get_node_set_map(tuple_list):
    """
    Function to get a mapping of random node names to values between 0
    and number of nodes - 1, with a modified adjacency list.

    Args:
        tuple_list : adjacency list with weights and arbitrary node names

    Returns:
        tuples : canonicalized adjacency list
        node_map : mapping from node name to index
    """
    node_set = set()
    for tpl in tuple_list:
        node_set.update(tpl[:2])
    node_map = {node_name: idx for idx, node_name in enumerate(node_set)}
    tuples = [(node_map[src], node_map[dst], wgt) for src, dst, wgt in tuple_list]
    return tuples, node_map


def edges_are_same(a, b):
    """
    Function to check if two tuple elements (src, tgt, val) correspond
    to the same directed edge (src, tgt).

    Args:
        tuple_elements : a = (src, val, val) and b = (src, val, val)

    Returns:
        True or False
    """
    if a[0:2] == b[0:2]:
        return True
    else:
        return False


def get_equivalent_edge(edges):
    """
    Function to obtain an equivalent directional edge between two nodes
    which have multiple edges in between. Also, assesses if edge is rendered neutral.

    Args:
        edges : List of tuple objects (src, val, val)
                with same 'src' and 'tgt' values and varying 'val' values

    Returns:
        equivalent_edge : Tuple object which represents the equivalent edge between
                          the given two nodes
        valid : True or False, based on whether the edge is valid or rendered to
                become neutral
    """
    mean = 0
    for edge in edges:
        mean += edge[2]
    if mean == 0:
        return (edges[0][0], edges[0][1], 0), False
    elif mean > 0:
        return (edges[0][0], edges[0][1], 1), True
    else:
        return (edges[0][0], edges[0][1], -1), True
