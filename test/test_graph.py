import unittest
from toydata.Graph import Graph

class testGraph(unittest.TestCase):
    def test_vertex(self):
        g = Graph()
        # insert
        u = g.insert_vertex('u')
        v = g.insert_vertex('v')
        w = g.insert_vertex('w')
        z = g.insert_vertex('z')
        self.assertEqual(g.vertex_count(), 4)
        self.assertEqual(''.join(str(n) for n in g.vertices()), 'uvwz')
        g.insert_edge(u, v)
        g.insert_edge(v, w)
        g.insert_edge(u, w)
        g.insert_edge(w, z)
        # degree
        self.assertEqual(g.degree(u), 2)
        self.assertEqual(g.degree(v), 2)
        self.assertEqual(g.degree(w), 3)
        self.assertEqual(g.degree(z), 1)
        # remove
        g.remove_vertex(u)
        self.assertEqual(g.vertex_count(), 3)
        self.assertEqual(''.join(str(n) for n in g.vertices()), 'vwz')

    def test_edges(self):
        g = Graph()
        u = g.insert_vertex('u')
        v = g.insert_vertex('v')
        w = g.insert_vertex('w')
        z = g.insert_vertex('z')
        uv = g.insert_edge(u, v)
        vw = g.insert_edge(v, w)
        # remove
        g.remove_edges(uv)
        self.assertIsNone(g.get_edge(u, v))
        self.assertEqual(''.join(str(n) for n in g.vertices()), 'uvwz')

    def test_dfs_bfs(self):
        g = Graph()
        # insert
        u = g.insert_vertex('u')
        v = g.insert_vertex('v')
        w = g.insert_vertex('w')
        z = g.insert_vertex('z')
        g.insert_edge(u, v)
        g.insert_edge(v, w)
        g.insert_edge(u, w)
        g.insert_edge(w, z)
        self.assertEqual(g.construct_path(u, w), [u, v, w])
        self.assertEqual(g.construct_path(u, z), [u, v, w, z])
        self.assertEqual(g.construct_path(u, w, False), [u, w])
        self.assertEqual(g.construct_path(u, z, False), [u, w, z])
