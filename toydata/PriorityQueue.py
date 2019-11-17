from toydata.utils import Empty
from toydata.PositionalList import PositionalList


# Composition design pattern
class PriorityQueueBase:
    """Abstract base class for a priority queue"""

    class _Item:
        """Lightweight composite to store priority queue items"""
        __slots__ = '_key', '_value'

        def __init__(self, k, v):
            self._key = k
            self._value = v

        # compare items based on there keys
        def __lt__(self, other):
            return self._key < other._key


class UnsortedPriorityQueue(PriorityQueueBase):
    """A min-oriented priority queue implemented with an unsorted list"""

    def __init__(self):
        """Create a new empty Priority Queue"""
        self._data = PositionalList()

    def __len__(self):
        return len(self._data)

    def __repr__(self):
        rep = '{'
        rep += ', '.join(f'({str(item._key)}, {str(item._value)})'
                         for item in self._data)
        rep += '}'
        return rep

    def is_empty(self):
        """Return True if the queue is empty"""
        return len(self) == 0

    def _find_min(self):
        """Return Position of item with minimum key"""
        if self.is_empty():
            raise Empty('Priority queue is empty')
        small = self._data.first()
        walk = self._data.after(small)
        while walk is not None:
            if walk.element() < small.element():
                small = walk
            walk = self._data.after(walk)
        return small

    def add(self, key, val):
        """Add a key-val pair"""
        self._data.add_last(self._Item(key, val))

    def min(self):
        """Return but do not remove (k, v) tuple with minimum key"""
        p = self._find_min()
        item = p.element()
        return (item._key, item._value)

    def remove_min(self):
        """Remove and return (k. v) tuple with minimum key"""
        p = self._find_min()
        item = self._data.delete(p)
        return (item._key, item._value)


class SortedPriorityQueue(PriorityQueueBase):
    """A min-oriented priority queue implemented with a sorted list"""

    def __init__(self):
        """Create a new empty Priority Queue"""
        self._data = PositionalList()

    def __len__(self):
        """Return the number of items in the priority queue"""
        return len(self._data)

    def __repr__(self):
        rep = '{'
        rep += ', '.join(f'({str(item._key)}, {str(item._value)})'
                         for item in self._data)
        rep += '}'
        return rep

    def is_empty(self):
        """Return True if the queue is empty"""
        return len(self) == 0

    def add(self, key, value):
        """Add a key-value pair"""
        newest = self._Item(key, value)
        walk = self._data.last()
        while walk and newest < walk.element():
            walk = self._data.before(walk)
        if walk is None:
            self._data.add_first(newest)
        else:
            self._data.add_after(walk, newest)

    def min(self):
        """Return but do not remove (k, v) tuple with minimum key"""
        if self.is_empty():
            raise Empty('Priority queue is empty')
        p = self._data.first()
        item = p.element()
        return (item._key, item._value)

    def remove_min(self):
        """Remove and return (k, v) tuple with minimum key"""
        if self.is_empty():
            raise Empty('Priority queue is empty')
        item = self._data.delete(self._data.first())
        return (item._key, item._value)


class HeapPriorityQueue(PriorityQueueBase):
    """A min-oriented priority queue implemented with a binary heap"""

    # public data
    def __init__(self):
        """Create a new empty Priority Queue"""
        self._data = []

    def __len__(self):
        """Return the number of items in the priority queue"""
        return len(self._data)

    def __repr__(self):
        rep = '{'
        rep += ', '.join(f'({str(item._key)}, {str(item._value)})'
                         for item in self._data)
        rep += '}'
        return rep

    def is_empty(self):
        """Return True if priority list is empty"""
        return len(self._data) == 0

    def add(self, key, value):
        """Add a key-value pair to the priority list"""
        self._data.append(self._Item(key, value))
        self._upheap(len(self._data) - 1)

    def min(self):
        if self.is_empty():
            raise Empty('Priority queue is empty')
        item = self._data[0]
        return (item._key, item._value)

    def remove_min(self):
        """Remove and return (k ,v) tuple with minimum key.
        Raise Empty exception if empty"""
        if self.is_empty():
            raise Empty('Priority queue is empty')
        self._swap(0, len(self._data) - 1)
        item = self._data.pop()
        self._downheadp(0)
        return (item._key, item._value)

    # non-public behaviors
    def _parent(self, j):
        return (j - 1) // 2

    def _left(self, j):
        return 2 * j + 1

    def _right(self, j):
        return 2 * j + 2

    # check index(beyond end or not)
    def _has_left(self, j):
        return self._left(j) < len(self._data)

    def _has_right(self, j):
        return self._right(j) < len(self._data)

    def _swap(self, i, j):
        """Swap the elements at indices i and j of array"""
        self._data[i], self._data[j] = self._data[j], self._data[i]

    def _upheap(self, j):
        parent = self._parent(j)
        if j > 0 and self._data[j] < self._data[parent]:
            self._swap(j, parent)
            self._upheap(parent)

    def _downheadp(self, j):
        if self._has_left(j):
            left = self._left(j)
            # although right may be smaller
            small_child = left
            if self._has_right(j):
                right = self._right(j)
                if self._data[right] < self._data[left]:
                    small_child = right
            if self._data[small_child] < self._data[j]:
                self._swap(small_child, j)
                self._downheadp(small_child)
