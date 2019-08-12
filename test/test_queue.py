import unittest
from toydata.Queue import ArrayQueue, LinkedQueue, ArrayDeque, LinkedDeque


class testArrayQueue(unittest.TestCase):
    def test_init(self):
        q = ArrayQueue()
        self.assertTrue(q.is_empty())

    def test_is_empty(self):
        q = ArrayQueue()
        self.assertTrue(q.is_empty())
        q.enqueue(1)
        self.assertFalse(q.is_empty())

    def test_first(self):
        q = ArrayQueue()
        q.enqueue(1)
        self.assertEqual(q.first(), 1)
        q.enqueue(2)
        self.assertEqual(q.first(), 1)

    def test_dequeue(self):
        q = ArrayQueue()
        q.enqueue(1)
        q.dequeue()
        self.assertTrue(q.is_empty)

    def test_enqueue(self):
        q = ArrayQueue()
        q.enqueue(1)
        self.assertEqual(q.first(), 1)


class testLinkedQueue(unittest.TestCase):
    def test_init(self):
        q = LinkedQueue()
        self.assertTrue(q.is_empty())

    def test_is_empty(self):
        q = LinkedQueue()
        self.assertTrue(q.is_empty())
        q.enqueue(1)
        self.assertFalse(q.is_empty())

    def test_first(self):
        q = LinkedQueue()
        q.enqueue(1)
        self.assertEqual(q.first(), 1)
        q.enqueue(2)
        self.assertEqual(q.first(), 1)

    def test_dequeue(self):
        q = LinkedQueue()
        q.enqueue(1)
        q.dequeue()
        self.assertTrue(q.is_empty)

    def test_enqueue(self):
        q = LinkedQueue()
        q.enqueue(1)
        self.assertEqual(q.first(), 1)


class testArrayDeque(unittest.TestCase):
    def test_add_last(self):
        q = ArrayDeque()
        q.add_last(1)
        self.assertEqual(q.last(), 1)

    def test_last(self):
        q = ArrayDeque()
        q.add_last(1)
        self.assertEqual(q.last(), 1)
        q.add_last(2)
        self.assertEqual(q.last(), 2)

    def test_delete_last(self):
        q = ArrayDeque()
        q.add_last(1)
        q.add_last(2)
        q.delete_last()
        self.assertEqual(q.last(), 1)

    def test_add_first(self):
        q = ArrayDeque()
        q.add_first(1)
        q.add_first(0)
        self.assertEqual(q.last(), 1)

    def test_first(self):
        q = ArrayDeque()
        q.add_first(1)
        self.assertEqual(q.first(), 1)

    def test_delete_first(self):
        q = ArrayDeque()
        q.add_last(1)
        q.add_first(0)
        q.delete_first()
        self.assertEqual(q.first(), 1)


class testLinkedDeque(unittest.TestCase):
    def test_first(self):
        q = LinkedDeque()
        q.insert_first(1)
        self.assertEqual(q.first(), 1)
        q.insert_first(2)
        self.assertEqual(q.first(), 2)
        q.delete_first()
        self.assertEqual(q.first(), 1)

    def test_last(self):
        q = LinkedDeque()
        q.insert_last(1)
        self.assertEqual(q.last(), 1)
        q.insert_last(2)
        self.assertEqual(q.last(), 2)
        q.delete_last()
        self.assertEqual(q.last(), 1)
