import unittest
from toydata.PositionalList import PositionalList


class testPositionalList(unittest.TestCase):
    def test_demo_exmples(self):
        L = PositionalList()
        self.assertTrue(L.is_empty())
        self.assertEqual(L.first(), None)
        L.add_last(8)
        self.assertFalse(L.is_empty())
        p = L.first()
        self.assertEqual(p._node._element, 8)
        q = L.add_after(p, 5)
        self.assertEqual(L.before(q), p)
        r = L.add_before(q, 3)
        self.assertEqual(r.element(), 3)
        self.assertEqual(L.after(p), r)
        self.assertEqual(L.before(p), None)
        L.add_first(9)
        self.assertEqual(L.delete(L.last()), 5)
        self.assertEqual(L.replace(p, 7), 8)
