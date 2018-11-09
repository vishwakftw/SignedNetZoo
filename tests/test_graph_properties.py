"""
Testing graph properties for graphs.
"""
import SSNA
import unittest
import numpy as np
import networkx as nx


class TestGraphDefs(unittest.TestCase):

    def setUp(self):
        self.G1 = nx.directed.random_uniform_k_out_graph(10, 3, self_loops=False)
        self.G2 = nx.directed.gn_graph(10)

    def test_get_adjacency_matrix(self):
        for graph in [self.G1, self.G2]:
            for meta_req in [True, False]:
                ret_val = SSNA.graph_properties.get_adjacency_matrix(graph, meta_req)
                self.assertIsInstance(ret_val, tuple)
                if not meta_req:
                    self.assertIsNone(ret_val[1])
                else:
                    self.assertIsInstance(ret_val[1], dict)
                    self.assertEqual(set(ret_val[1].keys()),
                                     {'density', 'positive', 'negative',
                                      'links', 'average_links'})
                self.assertEqual(ret_val[0].shape, (10, 10))

    def test_get_absolute_adjacency_matrix(self):
        for graph in [self.G1, self.G2]:
            mat = SSNA.graph_properties.get_absolute_adjacency_matrix(graph)
            self.assertTrue(all(mat.data > 0))
            self.assertEqual(mat.shape, (10, 10))

    def test_get_symmetric_adjacency_matrix(self):
        for graph in [self.G1, self.G2]:
            mat = SSNA.graph_properties.get_symmetric_adjacency_matrix(graph)
            self.assertEqual(mat.shape, (10, 10))
            self.assertFalse((mat != mat.T).todense().any())

    def test_get_absolute_symmetric_adjacency_matrix(self):
        for graph in [self.G1, self.G2]:
            mat = SSNA.graph_properties.get_absolute_symmetric_adjacency_matrix(graph)
            self.assertTrue(all(mat.data > 0))
            self.assertEqual(mat.shape, (10, 10))
            self.assertFalse((mat != mat.T).todense().any())

    def test_get_diagonal_degree_matrix(self):
        for graph in [self.G1, self.G2]:
            mat = SSNA.graph_properties.get_absolute_diagonal_degree_matrix(graph)
            self.assertTrue(all(mat.data > 0))
            self.assertEqual(mat.shape, (10, 10))
            self.assertTrue((np.diag(mat.diagonal()) == mat.todense()).all())

            mat = SSNA.graph_properties.get_absolute_symmetric_diagonal_degree_matrix(graph)
            self.assertTrue(all(mat.data > 0))
            self.assertEqual(mat.shape, (10, 10))
            self.assertTrue((np.diag(mat.diagonal()) == mat.todense()).all())


class TestClusteringCoeffs(unittest.TestCase):

    def setUp(self):
        self.G1 = nx.directed.random_uniform_k_out_graph(10, 3, self_loops=False)
        self.G2 = nx.directed.random_uniform_k_out_graph(20, 5, self_loops=False)

    def test_clustering_coeff(self):
        for graph in [self.G1, self.G2]:
            cc = SSNA.graph_properties.clustering_coeffs.clustering_coeff(graph)
            scc = SSNA.graph_properties.clustering_coeffs.sign_clustering_coeff(graph)
            rscc = SSNA.graph_properties.clustering_coeffs.relative_sign_clustering_coeff(graph)
            self.assertTrue(cc >= 0)
            self.assertTrue(abs(scc) <= cc)
            self.assertTrue(-1 <= rscc <= 1)


class TestBalanced(unittest.TestCase):

    def setUp(self):
        self.balanced_strong_undir = nx.Graph()
        self.balanced_strong_dir = nx.DiGraph()
        edges = [('A', 'B', 1), ('A', 'C', 1), ('A', 'E', -1), ('A', 'D', -1), ('D', 'E', 1)]
        self.balanced_strong_undir.add_weighted_edges_from(edges)
        self.balanced_strong_dir.add_weighted_edges_from(edges)

        self.unbalanced_undir = nx.Graph()
        self.unbalanced_dir = nx.DiGraph()
        edges = [('A', 'B', 1), ('A', 'C', 1), ('B', 'C', -1)]
        self.unbalanced_undir.add_weighted_edges_from(edges)
        self.unbalanced_dir.add_weighted_edges_from(edges)

        self.balanced_weak_undir = nx.Graph()
        self.balanced_weak_dir = nx.DiGraph()
        edges = [('A', 'B', -1), ('B', 'C', -1), ('C', 'D', -1), ('D', 'A', 1), ('B', 'D', -1)]
        self.balanced_weak_undir.add_weighted_edges_from(edges)
        self.balanced_weak_dir.add_weighted_edges_from(edges)

    def test_is_balanced(self):
        results_undir = []
        expected_results = [(True, {'strength': 'strong', 'possible_split': (['E', 'D'], ['A', 'B', 'C'])}),
                            (False, None),
                            (True, {'strength': 'weak', 'possible_split': None})]
        for i, graph in enumerate([self.balanced_strong_undir,
                                   self.unbalanced_undir,
                                   self.balanced_weak_undir]):
            result = SSNA.graph_properties.is_balanced(graph, True)
            self.assertEqual(result[0], expected_results[i][0])
            if expected_results[i][1] is not None:
                self.assertEqual(result[1]['strength'], expected_results[i][1]['strength'])
                self.assertEqual(result[1]['possible_split'], expected_results[i][1]['possible_split'])
            else:
                self.assertIsNone(result[1])


if __name__ == '__main__':
    unittest.main()
