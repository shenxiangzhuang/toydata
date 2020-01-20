import unittest
from toydata.Maps import ChainHashMap, ProbeHashMap, SortedTableMap


class testChainHashMap(unittest.TestCase):
    def test_add(self):
        t = ChainHashMap()
        with self.assertRaises(KeyError): t['a']
        t['a'] = 1
        self.assertEqual(t['a'], 1)

    def test_delete(self):
        t = ChainHashMap()
        t['a'] = 1
        del t['a']
        self.assertIsNone(t['a'])

    def test_change(self):
        t = ChainHashMap()
        t['a'] = 1
        t['a'] = 2
        self.assertEqual(t['a'], 2)


class testProbeHashMap(unittest.TestCase):
    def test_add(self):
        t = ProbeHashMap()
        with self.assertRaises(KeyError): t['a']
        t['a'] = 1
        self.assertEqual(t['a'], 1)

    def test_delete(self):
        t = ProbeHashMap()
        t['a'] = 1
        del t['a']
        with self.assertRaises(KeyError): t['a']

    def test_change(self):
        t = ProbeHashMap()
        t['a'] = 1
        t['a'] = 2
        self.assertEqual(t['a'], 2)


class testSortedTableMap(unittest.TestCase):
    def testSetGet(self):
        m = SortedTableMap()
        m['a'] = 1
        self.assertEqual(m['a'], 1)
        m['a'] = 2
        self.assertEqual(m['a'], 2)
    
    def testDel(self):
        m = SortedTableMap()
        m['a'] = 1
        del m['a']
        with self.assertRaises(KeyError): m['a']
        with self.assertRaises(KeyError): m['b']
    
    def testFind(self):
        m = SortedTableMap()
        m['a'] = 1
        m['c'] = 3
        m['b'] = 2
        self.assertEqual(m.find_min(), ('a', 1))
        self.assertEqual(m.find_max(), ('c', 3))
        m['e'] = 5
        self.assertEqual(m.find_ge('d'), ('e', 5))
        self.assertEqual(m.find_lt('d'), ('c', 3))
        self.assertEqual(m.find_lt('c'), ('b', 2))
        self.assertEqual(m.find_gt('c'), ('e', 5))
        self.assertEqual(m.find_gt('d'), ('e', 5))
        self.assertEqual(list(m.find_range('a', 'e')),
                        [('a', 1), ('b', 2), ('c', 3)])
        self.assertEqual(list(m.find_range('a', 'd')),
                        [('a', 1), ('b', 2), ('c', 3)])

    def testPrint(self):
        m = SortedTableMap()
        m['a'] = 1
        m['c'] = 3
        m['b'] = 2
