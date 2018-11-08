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


if __name__ == '__main__':
    unittest.main()
