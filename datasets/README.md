# Alternate Datasets
The current directory has a list of various alternative signed directed social network graphs:

***Readme:*** All the datasets and pickles have been ignored in the repository. Running the script `extract_graphs.py` will download, process and export pickles of each social network graph into `/pickles`.

- **[Bitcoin OTC Trust Weighted Signed Network:](https://snap.stanford.edu/data/soc-sign-bitcoin-otc.html)** This is who-trusts-whom network of people who trade using Bitcoin on a platform called Bitcoin OTC. Since Bitcoin users are anonymous, there is a need to maintain a record of users' reputation to prevent transactions with fraudulent and risky users. Members of Bitcoin OTC rate other members in a scale of -10 (total distrust) to +10 (total trust) in steps of 1. This is the first explicit weighted signed directed network available for research.

   Dataset Download Link: [soc-sign-bitcoinotc.csv.gz](https://snap.stanford.edu/data/soc-sign-bitcoinotc.csv.gz)

- **[Epinions Social Network:](https://snap.stanford.edu/data/soc-sign-epinions.html)** This is who-trust-whom online social network of a a general consumer review site Epinions.com. Members of the site can decide whether to ''trust'' each other. All the trust relationships interact and form the Web of Trust which is then combined with review ratings to determine which reviews are shown to the user.

   Dataset Download Link: [soc-sign-epinions.txt.gz](https://snap.stanford.edu/data/soc-sign-epinions.txt.gz)

- **[Wikipedia Requests for Adminship:](https://snap.stanford.edu/data/wiki-RfA.html)** For a Wikipedia editor to become an administrator, a request for adminship (RfA) must be submitted, either by the candidate or by another community member. Subsequently, any Wikipedia member may cast a supporting, neutral, or opposing vote.

   Dataset Download Link: [wiki-RfA.txt.gz](https://snap.stanford.edu/data/wiki-RfA.txt.gz)

The pickled graph objects of each of these dataset is stored in `/pickles`. These can be imported into any specific program using `G = nx.read_gpickle("pth_to_pickle")`.
