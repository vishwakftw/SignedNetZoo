import urllib.request
import os.path
from os.path import basename

folder_paths = ["Bitcoin-OTC-Trust-Network",
                "Epinions-Social-Network",
                "Wikipedia-Requests-for-Adminship"]

dl_links = ["https://snap.stanford.edu/data/soc-sign-bitcoinotc.csv.gz",
            "https://snap.stanford.edu/data/soc-sign-epinions.txt.gz",
            "https://snap.stanford.edu/data/wiki-RfA.txt.gz"]

def download_file(path, link):
    filename = basename(link)
    local_path = path + "/" + filename
    if os.path.isfile(local_path):
        print("- File already downloaded.")
        return
    print("- Downloading: " + filename + "...")
    urllib.request.urlretrieve (link, local_path)
    print("- " + filename + " has been downloaded.")
    return

def extract_file(path, link):
    filename = basename(link)
    pickle_path = "pickles/" + filename.split('.')[0] + ".gpickle"
    if os.path.isfile(pickle_path):
        print("- Pickle already extracted.")
        return
    print("- Processing and Extracting graph: " + filename + "...")
    os.chdir(path)
    os.system("python extract_graph.py")
    os.chdir("..")
    return


def main():
    for index, path in enumerate(folder_paths):
        print("----------------------------------------")
        print(path)
        print("----------------------------------------")
        download_file(path, dl_links[index])
        extract_file(path, dl_links[index])
    print("----------------------------------------")


main()
