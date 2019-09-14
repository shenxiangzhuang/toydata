import unittest
from toydata.Maps import ChainHashMap, ProbeHashMap


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
