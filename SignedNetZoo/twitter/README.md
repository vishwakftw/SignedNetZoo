# Sentiment140 Dataset &rarr; Signed Twitter Network

**Sentiment140 Dataset:** This dataset contains 1,600,000 tweets extracted using the Twitter API. The tweets have been annotated (0 = negative, 2 = neutral, 4 = positive) and they can be used to detect sentiment.

The iPython Notebook in this directory describes the process of analysis of the Sentiment140 Dataset and eventual conversion into a signed Twitter network.

### Graph Conversion

- All of the 1,600,000 tweets only consist of **postive** or **negative** sentiment tweets.
- There are **659,775 distinct source users** who tweeted the total of 1,600,000 tweets.
- There are a total of **703,311 tweets** directed to **single other users**.
- There are a total of **33,194 tweets** directed to **multiple other users**.
- As semantic implication of the sentiment of multi-directed tweets is unpredictable, only **uni-directed tweets (703,311)** are considered.
- There are **293,410 distinct source users** who tweeted a total of 703,311 tweets directed to among **334,272 distinct target users**.
- There a total of **96,584 common users** among these 2 sets.
- We have a hashmap for a user base of **531098 individuals**. Also, 531098 = 293410 + 334272 - 96584.
- By generating a graph with these 703,311 tweets as edges, where we render multiple edges between two nodes equivalent to the majority of the sentiment. If an edge ends up having a neutral effective sentiment, it is removed from the graph. We are left with **566,173 edges**.
- Finally, our **NetworkX graph object** is exported with **566,173 edges**.


The same implentation is incorporated within [`SignedNetZoo/datasets/Twitter.py`](https://github.com/vishwakftw/SignedNetZoo/blob/master/SignedNetZoo/datasets/Twitter.py) allowing smooth graph generation within the package.
