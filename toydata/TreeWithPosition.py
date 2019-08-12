"""
Note that, the code here comes from Michael's book: Data Structures
and Algorithms in Python.But we do *not* use it in our *toydata* package,
because I think the usage of Position classis confusing and not intuitive
in a way.

So we just put the code here for reference and implement the tree
in another way.
"""


from abc import ABCMeta, abstractmethod
from typing import Iterator
from toydata.Queue import LinkedQueue


class Tree(metaclass=ABCMeta):
    """Abstract base class representing a tree structure."""

    # nested Position class
    class Position(metaclass=ABCMeta):
        """An abstraction representation the location of a single element."""
        @abstractmethod
        def element(self):
            """Return the element store at this Position"""

        @abstractmethod
        def __eq__(self, other):
            """Return True if other Position represent the same location"""

        def __ne__(self, other):
            """Return True if other does not represent the same location"""
            return not (self == other)

    # Some abstract methods that concrete subclass must support
    @abstractmethod
    def root(self):
        """Return Position representing the tree's root(or None if empty)"""

    @abstractmethod
    def parent(self, p):
        """Return Position representing p's parent(or None if p is root)"""

    @abstractmethod
    def num_children(self, p):
        """Return the number of children that Position p has"""

    @abstractmethod
    def children(self, p) -> Iterator:
        """Generate an iteration of Positions representing p's children"""

    @abstractmethod
    def __len__(self):
        """Return the total number of element in the tree"""

    # Some concrete methods implemented in the class
    def is_root(self, p):
        """Return True if Position p represent the root of the tree"""
        return self.root() == p

    def is_leaf(self, p):
        """Return True if Position p does not have any children"""
        return self.num_children(p) == 0

    def is_empty(self):
        """Return True if the tree is empty"""
        return self.__len__() == 0

    def depth(self, p):
        """Return the number of levels separating Position p from the root

        Top -> Bottom

        Time complexity: O(d_p + 1)
        """
        if self.is_root(p):
            return 0
        else:
            return 1 + self.depth(self.parent(p))

    def _height(self, p):
        """Return the height of the subtree rooted at Position p"""
        if self.is_leaf(p):
            return 0
        else:
            return 1 + max(self._height(c) for c in self.children(p))

    def height(self, p=None):
        """Return the height of the subtree rooted at Position P.

        If p is None ,return the height of the entire tree

        Time complexity: O(n)
        """
        if p is None:
            p = self.root()
        return self._height(p)

    # Implementing Tree Traversals
    def preorder(self):
        """Generate a preorder iteration of positions in the tree."""
        if not self.is_empty():
            for p in self._subtree_preorder(self.root()):
                yield p

    def _subtree_preorder(self, p):
        """Generate a preorder iteration of positions
        in subtree rooted at p."""
        yield p
        for c in self.children(p):
            for other in self._subtree_preorder(c):
                yield other

    def postorder(self):
        """Generate a postorder iteration of positions in the tree."""
        if not self.is_empty():
            for p in self._subtree_postorder(self.root()):
                yield p

    def _subtree_postorder(self, p):
        """Generate a postorder iteration of positions
        in subtree rooted at p."""
        for c in self.children(p):
            for other in self._subtree_postorder(c):
                yield other
        yield p

    def breadthfirst(self):
        """Generate a breath-first iteration of the positions of the tree"""
        if not self.is_empty():
            fringe = LinkedQueue()
            fringe.enqueue(self.root())
            while not fringe.is_empty():
                p = fringe.dequeue()
                yield p
                for c in self.children(p):
                    fringe.enqueue(c)


class BinaryTree(Tree):
    """Abstract base class representing a binary tree structure"""
    # additional abstract methods
    def left(self, p):
        """Return a Position representing p's left child

        Return None if p does not have a left child
        """
        raise NotImplementedError('must be implemented by subclass')

    def right(self, p):
        """Return a Position representing p's right child

        Return None if p does not have a right child
        """
        raise NotImplementedError('must be implemented by subclass')

    # concrete methods implemented in this class
    def sibling(self, p):
        """Return a Position representing p's sibling(or None if no sibling)"""
        parent = self.parent(p)
        if parent is None:  # p is the root
            return None
        else:
            if p == self.left(parent):
                return self.right(parent)
            else:
                return self.left(parent)

    def children(self, p):
        """Generate an iteration of Positions representing p's children"""
        if self.left(p) is not None:
            yield self.left(p)
        if self.right(p) is not None:
            yield self.right(p)

    # In-order iteration
    def inorder(self):
        """Generate an inorder iteration of positions in the tree"""
        if not self.is_empty():
            for p in self._subtree_inorder(self.root()):
                yield p

    def _subtree_inorder(self, p):
        """Generate an inorder iteration of positions in the tree"""
        if self.left(p) is not None:
            for other in self._subtree_inorder(self.left(p)):
                yield other
        yield p
        if self.right(p) is not None:
            for other in self._subtree_inorder(self.right(p)):
                yield other

    # positions and itertation
    def positions(self, trav_method='preorder'):
        """Generate an iteration of the tree's positions

        Methods: preorder, postorder, breadthfirst, inorder
        """
        if trav_method == 'preorder':
            return self.preorder()
        elif trav_method == 'postorder':
            return self.postorder()
        elif trav_method == 'breathfirst':
            return self.breadthfirst()
        elif trav_method == 'inorder':
            return self.inorder()

    def __iter__(self):
        """Generate an iteration of the tree's elements"""
        for p in self.positions():
            yield p.element()


class LinkedBinaryTree(BinaryTree):
    """Linked representation of a binary tree structure"""

    class _Node:
        """Lightweight, nonpublic class for storing a node"""
        __slots__ = '_element', '_parent', '_left', '_right'

        def __init__(self, element, parent=None, left=None, right=None):
            self._element = element
            self._parent = parent
            self._left = left
            self._right = right

    class Position(BinaryTree.Position):
        """An abstraction representing the location of a single element"""

        def __init__(self, container, node):
            """Constructor should not be invoked by user"""
            self._container = container
            self._node = node

        def __str__(self):
            return str(self._node._element)

        def element(self):
            """Return the element at this Position"""
            return self._node._element

        def __eq__(self, other):
            """Return True if other is a Position representing
            the same location"""
            return type(other) is type(self) and other._node is self._node

    def _validate(self, p):
        """Return associated node, if position is valid"""
        if not isinstance(p, self.Position):
            raise TypeError('p must be proper Position type')
        if p._container is not self:
            raise ValueError('p does not belong to this container')
        if p._node._parent is p._node:  # convention for deprecated nodes
            raise ValueError('p is no longer valid')
        return p._node

    def _make_position(self, node):
        """Return Position instance for given node(or None if no node)"""
        return self.Position(self, node) if node is not None else None

    # binary tree constrcture
    def __init__(self, root=None):
        """Create an initially empty binary tree"""
        self._root = root
        self._size = 0

    # public access
    def __len__(self):
        """Return the total number of elements in the tree

        Time complexity: O(1)
        """
        return self._size

    # printing
    def __str__(self):
        pass

    def root(self):
        """Return the root Position of the tree(or None if tree is empty)

        Time complexity: O(1)
        """
        return self._make_position(self._root)

    def parent(self, p):
        """Return the Position of p's parent(or None if p is root)

        Time complexity: O(1)
        """
        node = self._validate(p)
        return self._make_position(node._parent)

    def left(self, p):
        """Return the Position of p's left child(or None if no left child)

        Time complexity: O(1)
        """
        node = self._validate(p)
        return self._make_position(node._left)

    def right(self, p):
        """Return the Position of p's right child(or None if no right child)

        Time complexity: O(1)
        """
        node = self._validate(p)
        return self._make_position(node._right)

    def num_children(self, p):
        """Return the number of children of Position p

        Time complexity: O(1)
        """
        node = self._validate(p)
        count = 0
        if node.left is not None:
            count += 1
        if node._right is not None:
            count += 1
        return count

    # nonpublic mutators
    def _add_root(self, e):
        """Place element e at the root of an empty tree and return new Position.

        Raise ValueError if tree nonempty.

        Time complexity: O(1)
        """
        if self._root is not None:
            raise ValueError('Root exists')
        self._size = 1
        self._root = self._Node(e)
        return self._make_position(self._root)

    def _add_left(self, p, e):
        """Create a new left child for Position p, storing element e.

        Return the Position of new node.
        Raise ValueError if Position p is invalid or p already has a
        left child.

        Time complexity: O(1)
        """
        node = self._validate(p)
        if node._left is not None:
            raise ValueError('Left child exists')
        self._size += 1
        # node is its parent
        node._left = self._Node(e, node)
        return self._make_position(node._left)

    def _add_right(self, p, e):
        """Create a new right child for Position p, storing element e.

        Return the Position of new node.
        Raise ValueError if Position p is invalid or
        p already has a right child.

        Time complexity: O(1)
        """
        node = self._validate(p)
        if node._right is not None:
            raise ValueError('Right child exists')
        self._size += 1
        # node is its parent
        node._right = self._Node(e, node)
        return self._make_position(node._right)

    def _replace(self, p, e):
        """Replace the element at position p with e, and return old element.

        Time complexity: O(1)
        """
        node = self._validate(p)
        old = node._element
        node._element = e
        return old

    def _delete(self, p):
        """Delete the node at Position p, and replace it with its child, if any.

        Return the element that had been stored at Position p.
        Raise ValueError if Position p is invalid or p has two children.

        Time complexity: O(1)
        """
        node = self._validate(p)
        if self.num_children(p) == 2:
            raise ValueError('Position has two children')
        child = node._left if node._left else node._right  # might be None
        if child is not None:
            child._parent = node._parent   # child's grandparent becomes parent
        if node is self._root:
            self._root = child             # child becomes root
        else:
            parent = node._parent
            if node is parent._left:
                parent._left = child
            else:
                parent._right = child
        self._size -= 1
        node._parent = node              # convention for deprecated node
        return node._element

    def _attach(self, p, t1, t2):
        """Attach trees t1 and t2, respectively, as the left and right
        subtrees of the external Position p.

        As a side effect, set t1 and t2 to empty.
        Raise TypeError if trees t1 and t2 do not match type of this tree.
        Raise ValueError if Position p is invalid or not external.

        Time complexity: O(1)
        """
        node = self._validate(p)
        if not self.is_leaf(p):
            raise ValueError('position must be leaf')
        # all 3 trees must be same type
        if not type(self) is type(t1) is type(t2):
            raise TypeError('Tree types must match')
        self._size += len(t1) + len(t2)
        # attached t1 as left subtree of node
        if not t1.is_empty():
            t1._root._parent = node
            node._left = t1._root
            t1._root = None             # set t1 instance to empty
            t1._size = 0
        if not t2.is_empty():         # attached t2 as right subtree of node
            t2._root._parent = node
            node._right = t2._root
            t2._root = None             # set t2 instance to empty
            t2._size = 0
