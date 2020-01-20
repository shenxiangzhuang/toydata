import unittest
from toydata.Tree import LinkedBinaryTree


class testTree(unittest.TestCase):
    def test_init(self):
        t1 = LinkedBinaryTree()
        self.assertIsNone(t1._root)
        self.assertEqual(len(t1), 0)
        t1._add_root(1)
        self.assertEqual(t1.root().element(), 1)
        self.assertEqual(len(t1), 1)
        # another way
        t2 = LinkedBinaryTree(2)
        self.assertEqual(t2.root().element(), 2)
        self.assertEqual(len(t2), 1)

    def test_add(self):
        t = LinkedBinaryTree(1)
        t._add_left(t.root(), 2)
        t._add_right(t.root(), 3)
        self.assertEqual(t.root().element(), 1)
        self.assertEqual(t.left(t.root()).element(), 2)
        self.assertEqual(t.right(t.root()).element(), 3)
        self.assertEqual(len(t), 3)
        # contine
        t21 = t._add_left(t.left(t.root()), 21)
        t22 = t._add_right(t.left(t.root()), 22)
        t31 = t._add_left(t.right(t.root()), 31)
        t32 = t._add_right(t.right(t.root()), 32)
        self.assertEqual(t21.element(), 21)
        self.assertEqual(t22.element(), 22)
        self.assertEqual(t31.element(), 31)
        self.assertEqual(t32.element(), 32)
        self.assertEqual(len(t), 7)

    def test_replace(self):
        t = LinkedBinaryTree(1)
        t._replace(t.root(), 2)
        self.assertEqual(t.root().element(), 2)
        tl = t._add_left(t.root(), 3)
        self.assertEqual(tl.element(), 3)
        t._replace(t.left(t.root()), 4)
        self.assertEqual(tl.element(), 4)

    def test_delete(self):
        t = LinkedBinaryTree(1)
        t._delete(t.root())
        self.assertIsNone(t._root)
        t._add_root(1)
        t._add_left(t.root(), 2)
        self.assertEqual(len(t), 2)
        t._delete(t.root())
        self.assertEqual(t.root().element(), 2)
        self.assertEqual(len(t), 1)
    
    def test_print(self):
        t = LinkedBinaryTree(1)
        t._add_left(t.root(), 2)
        t._add_right(t.root(), 3)
        t._add_left(t.left(t.root()), 21)
        t._add_right(t.left(t.root()), 22)
        t._add_left(t.right(t.root()), 31)
        t._add_right(t.right(t.root()), 32)
        s = '1\n  2\n    21\n    22\n  3\n    31\n    32\n'
        self.assertEqual(str(t), s)
