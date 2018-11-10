"""
Smoke test for datasets in SignedNetZoo.
"""
import SignedNetZoo
import shutil
import unittest
import networkx as nx


class TestDataset(unittest.TestCase):

    @staticmethod
    def _test_dataset(self, dataset_name):

        root = './data'
        # First test without split
        dataset = getattr(SignedNetZoo.datasets, dataset_name)(root=root)
        G = dataset.graph
        self.assertIsInstance(G, nx.DiGraph)
        n_edges = G.number_of_edges()
        n_nodes = G.number_of_nodes()
        shutil.rmtree(root)

        for split in [0.7, 0.8, 0.9]:
            # Now test with splits
            dataset = getattr(SignedNetZoo.datasets, dataset_name)(root=root, split=split)
            G_train, G_test = dataset.graph
            self.assertIsInstance(G_train, nx.DiGraph)
            self.assertIsInstance(G_test, nx.DiGraph)

            n_train_edges = G_train.number_of_edges()
            n_test_edges = G_test.number_of_edges()

            n_train_nodes = G_train.number_of_nodes()
            n_test_nodes = G_test.number_of_nodes()

            self.assertEqual(n_train_edges + n_test_edges, n_edges)
            self.assertEqual(n_train_nodes, n_nodes)
            self.assertEqual(n_test_nodes, n_nodes)
            shutil.rmtree(root)

    def test_bitcoin(self):
        self._test_dataset(self, 'Bitcoin')

    def test_epinions(self):
        self._test_dataset(self, 'Epinions')

    def test_slashdotzoo(self):
        self._test_dataset(self, 'SlashdotZoo')

    def test_twitter(self):
        self._test_dataset(self, 'Twitter')

    def test_wikipedia(self):
        self._test_dataset(self, 'Wikipedia')

    def test_wikisigned(self):
        self._test_dataset(self, 'WikiSigned')


if __name__ == '__main__':
    unittest.main()
