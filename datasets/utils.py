from tqdm import tqdm

import urllib.request
import os


def gen_bar_updater(pbar):
    def bar_update(count, block_size, total_size):
        if pbar.total is None and total_size:
            pbar.total = total_size
        progress_bytes = count * block_size
        pbar.update(progress_bytes - pbar.n)

    return bar_update

def download_file(path, link):
    local_path = os.path.join(path, os.path.basename(link))
    if os.path.isfile(local_path):
        print("- File already downloaded.")
        return
    urllib.request.urlretrieve(link, local_path, reporthook=gen_bar_updater(tqdm(unit='B', unit_scale=True)))
