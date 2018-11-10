# Datasets
The current directory has a list of various signed directed social network graphs including Slashdot Zoo.

### Usage
- Pertaining to each dataset is a class. For example, the `SlashdotZoo` class in [`SlashdotZoo.py`](https://github.com/vishwakftw/CS6270-TDBMS/blob/master/datasets/SlashdotZoo.py) is for the Slashdot Zoo dataset.

- Certaining an instance of this class will download the dataset, create a `Networkx` graph object, and pickle it. This pickle will be used later for getting the graphs (since the graphs are pretty heavy memory-wise). Arguments for instantiating would just be a `root` argument - which is the location where the datasets and the corresponding graph pickle is stored.

- To get the `Networkx` graph object after instantiation, one will have to do `<instance>.graph` (which is a property of the class).

- URLs for the datasets are properties of the class which represent them, and can be obtained by `<instance>.url`.

### Description of the Datasets

- **[Slashdot Zoo:](http://konect.cc/networks/slashdot-zoo/)** This is the signed social network of users of the technology news site Slashdot (slashdot.org), connected by directed "friend" and "foe" relations. The "friend" and "foe" labels are used on Slashdot to mark users, and influence the scores as seen by each user. For instance, If user A marks user B as a foe, the score of user B's posts will be decreased as shown to user A. 

- **[Bitcoin OTC Trust Weighted Signed Network:](https://snap.stanford.edu/data/soc-sign-bitcoin-otc.html)** This is who-trusts-whom network of people who trade using Bitcoin on a platform called Bitcoin OTC. Since Bitcoin users are anonymous, there is a need to maintain a record of users' reputation to prevent transactions with fraudulent and risky users. Members of Bitcoin OTC rate other members in a scale of -10 (total distrust) to +10 (total trust) in steps of 1. This is the first explicit weighted signed directed network available for research.

- **[Epinions Social Network:](https://snap.stanford.edu/data/soc-sign-epinions.html)** This is who-trust-whom online social network of a a general consumer review site Epinions.com. Members of the site can decide whether to ''trust'' each other. All the trust relationships interact and form the Web of Trust which is then combined with review ratings to determine which reviews are shown to the user.

- **[Wikipedia Requests for Adminship:](https://snap.stanford.edu/data/wiki-RfA.html)** For a Wikipedia editor to become an administrator, a request for adminship (RfA) must be submitted, either by the candidate or by another community member. Subsequently, any Wikipedia member may cast a supporting, neutral, or opposing vote.

- **[WikiSigned:](http://konect.uni-koblenz.de/networks/wikisigned-k2)** This undirected signed network contains interpreted interactions between the users of the English Wikipedia that have edited pages about politics. The dataset is based on a set of 563 articles from the politics domain of the English Wikipedia.
