import unittest
from toydata.Stack import ArrayStack


class testArrayStack(unittest.TestCase):
    def test_push(self):
        s = ArrayStack()
        s.push(1)
        self.assertEqual(s.top(), 1)
        s.push(2)
        self.assertEqual(s.top(), 2)

    def test_pop(self):
        s = ArrayStack()
        s.push(1)
        self.assertEqual(s.pop(), 1)
        s.push(2)
        s.push(3)
        s.pop()
        self.assertEqual(s.top(), 2)
