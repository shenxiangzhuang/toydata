import unittest
from toydata.PriorityQueue import UnsortedPriorityQueue, Empty
from toydata.PriorityQueue import SortedPriorityQueue, HeapPriorityQueue


class testUnsortedPriorityQueue(unittest.TestCase):
    def test_demo_exmples(self):
        P = UnsortedPriorityQueue()
        self.assertTrue(P.is_empty())
        P.add(5, 'A')
        self.assertFalse(P.is_empty())
        self.assertEqual(repr(P), "{(5, A)}")
        P.add(9, 'C')
        P.add(3, 'B')
        P.add(7, 'D')
        self.assertEqual(P.min(), (3, 'B'))
        self.assertEqual(P.remove_min(), (3, 'B'))
        self.assertEqual(P.remove_min(), (5, 'A'))
        self.assertEqual(len(P), 2)
        self.assertEqual(P.remove_min(), (7, 'D'))
        self.assertEqual(P.remove_min(), (9, 'C'))
        self.assertTrue(P.is_empty())
        self.assertRaises(Empty, P.remove_min)


class testSortedPriorityQueue(unittest.TestCase):
    def test_demo_exmples(self):
        P = SortedPriorityQueue()
        self.assertTrue(P.is_empty())
        P.add(5, 'A')
        self.assertFalse(P.is_empty())
        self.assertEqual(repr(P), "{(5, A)}")
        P.add(9, 'C')
        P.add(3, 'B')
        P.add(7, 'D')
        self.assertEqual(P.min(), (3, 'B'))
        self.assertEqual(P.remove_min(), (3, 'B'))
        self.assertEqual(P.remove_min(), (5, 'A'))
        self.assertEqual(len(P), 2)
        self.assertEqual(P.remove_min(), (7, 'D'))
        self.assertEqual(P.remove_min(), (9, 'C'))
        self.assertTrue(P.is_empty())
        self.assertRaises(Empty, P.remove_min)


class testHeapPriorityQueue(unittest.TestCase):
    def test_demo_exmples(self):
        P = HeapPriorityQueue()
        self.assertTrue(P.is_empty())
        P.add(5, 'A')
        self.assertFalse(P.is_empty())
        self.assertEqual(repr(P), "{(5, A)}")
        P.add(9, 'C')
        P.add(3, 'B')
        P.add(7, 'D')
        self.assertEqual(P.min(), (3, 'B'))
        self.assertEqual(P.remove_min(), (3, 'B'))
        self.assertEqual(P.remove_min(), (5, 'A'))
        self.assertEqual(len(P), 2)
        self.assertEqual(P.remove_min(), (7, 'D'))
        self.assertEqual(P.remove_min(), (9, 'C'))
        self.assertTrue(P.is_empty())
        self.assertRaises(Empty, P.remove_min)
