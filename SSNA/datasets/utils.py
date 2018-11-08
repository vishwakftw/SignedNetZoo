from tqdm import tqdm

import urllib.request
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
    urllib.request.urlretrieve(link, local_path, reporthook=gen_bar_updater(tqdm(unit='B', unit_scale=True)))


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
