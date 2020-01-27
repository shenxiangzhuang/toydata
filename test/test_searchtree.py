import unittest
from toydata.SearchTree import AVLTreeMap, SplayTreeMap, RedBlackTreeMap


class testAVLTreeMap(unittest.TestCase):
    def test_insert(self):
        t = AVLTreeMap()
        t[1] = 'a'
        t[2] = 'b'
        t[3] = 'c'
        self.assertEqual(t[1], 'a')
        self.assertEqual(t[2], 'b')
        self.assertEqual(t[3], 'c')
        self.assertEqual(str(t), '(2:b)\n  (1:a)\n  (3:c)\n')

    def test_change(self):
        t = AVLTreeMap()
        t[1] = 'a'
        t[2] = 'b'
        t[3] = 'c'
        self.assertEqual(t[3], 'c')
        t[3] = 'cc'
        self.assertEqual(t[3], 'cc')

    def test_delete(self):
        t = AVLTreeMap()
        t[1] = 'a'
        t[2] = 'b'
        t[3] = 'c'
        self.assertEqual(t[3], 'c')
        del t[3]
        with self.assertRaises(KeyError): t[3]


class testSplayTreeMap(unittest.TestCase):
    def test_insert(self):
        t = SplayTreeMap()
        t[1] = 'a'
        t[2] = 'b'
        t[3] = 'c'
        self.assertEqual(t[1], 'a')
        self.assertEqual(t[2], 'b')
        self.assertEqual(t[3], 'c')

    def test_change(self):
        t = SplayTreeMap()
        t[1] = 'a'
        t[2] = 'b'
        t[3] = 'c'
        self.assertEqual(t[3], 'c')
        t[3] = 'cc'
        self.assertEqual(t[3], 'cc')

    def test_delete(self):
        t = SplayTreeMap()
        t[1] = 'a'
        t[2] = 'b'
        t[3] = 'c'
        self.assertEqual(t[3], 'c')
        del t[2]
        with self.assertRaises(KeyError): t[2]


class testRedBlackTreeMap(unittest.TestCase):
    def test_insert(self):
        t = RedBlackTreeMap()
        t[1] = 'a'
        t[2] = 'b'
        t[3] = 'c'
        self.assertEqual(t[1], 'a')
        self.assertEqual(t[2], 'b')
        self.assertEqual(t[3], 'c')

    def test_change(self):
        t = RedBlackTreeMap()
        t[1] = 'a'
        t[2] = 'b'
        t[3] = 'c'
        self.assertEqual(t[3], 'c')
        t[3] = 'cc'
        self.assertEqual(t[3], 'cc')

    def test_delete(self):
        t = RedBlackTreeMap()
        t[1] = 'a'
        t[2] = 'b'
        t[3] = 'c'
        self.assertEqual(t[3], 'c')
        del t[2]
        with self.assertRaises(KeyError): t[2]
