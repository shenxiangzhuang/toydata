from toydata.utils import Empty
from toydata.LinkedLists import Singlellist


class ArrayQueue:
    """
    FIFO queue implementation using Python list
    as unedrlying storage.
    """
    # moderate capacity for all new queues
    DEFAULT_CAPACITY = 10

    def __init__(self):
        """Create an empty queue"""
        self._data = [None] * ArrayQueue.DEFAULT_CAPACITY
        self._size = 0
        self._font = 0

    def __len__(self):
        """Return the number of elements in the queue

        Time complexity: O(1)
        """
        return self._size

    def __str__(self):
        """Show the Queue properly

        Time complexity: O(n)
        """
        if self.is_empty():
            return "Empty Queue"
        s = []
        for index, ele in enumerate(self._data):
            back = (self._font + self._size - 1) % len(self._data)
            if ele is None:
                ele_str = f"| None |"
            # back and font
            elif index == self._font == back:
                ele_str = "| " + f"->{str(ele)}<-".center(5) + " |"
            # font
            elif index == self._font:
                ele_str = "| " + f"->{str(ele)}".center(5) + " |"
            # back
            elif index == back:
                ele_str = "| " + f"{str(ele)}<-".center(5) + " |"
            else:
                ele_str = "| " + f"{str(ele)}".center(5) + " |"
            s.append(ele_str)
        return ''.join(s)

    def is_empty(self):
        """Return True if the queue is empty

        Time complexity: O(1)
        """
        return self._size == 0

    def first(self):
        """
        Return the first element.
        Raise Empty Error if the queue is empty

        Time complexity: O(1)
        """
        if self.is_empty():
            raise Empty("Queue is empty!")
        return self._data[self._font]

    def dequeue(self):
        """
        Remove and return the first element.
        Raise Empty error if queue is empty

        Time complexity: O(1)*


        Note that `*` means amortized.
        """
        if self.is_empty():
            raise Empty("Queue is empty!")
        answer = self._data[self._font]
        # help garbage collection
        self._data[self._font] = None
        self._font = (self._font + 1) % len(self._data)
        self._size -= 1
        # shrinks
        if 0 < self._size < len(self._data) // 4:
            self._resize(len(self._data) // 2)
        return answer

    def enqueue(self, e):
        """
        Add an element to the back of the queue

        Time complexity: O(1)*
        """
        if len(self._data) == self._size:
            self._resize(len(self._data) * 2)
        avail = (self._font + self._size) % len(self._data)
        self._data[avail] = e
        self._size += 1

    def _resize(self, cap):
        """
        Resize to a new list of capacity >= len(self)
        Note: we assume cap > len(self)

        Time complexity: O(n)
        """
        old = self._data
        self._data = [None] * cap
        walk = self._font
        for i in range(self._size):
            self._data[i] = old[walk]
            walk = (walk + 1) % len(old)
        self._font = 0


class LinkedQueue(Singlellist):
    """FIFO queue implementation using a single linked list for storage"""
    def __init__(self):
        """Create an empty queue"""
        self._data = Singlellist()

    def __len__(self):
        """Return the number of elements in the queue"""
        return len(self._data)

    def is_empty(self):
        """Return True if the queue is empty"""
        return len(self._data) == 0

    def first(self):
        """Return(but do not remove) the element at the front if the queue"""
        if self.is_empty():
            raise Empty("Queue is empty")
        return self._data.head.value

    def dequeue(self):
        """Remove and return the first element if the queue(i.e., FIFO).

        Raisee Empty exception if the dueue is empty"""
        if self.is_empty():
            raise Empty("Queue is empty")
        node = self._data.remove_first()
        return node.value

    def enqueue(self, e):
        """Add an element to the back of the queue"""
        self._data.add_last(e)


class ArrayDeque(ArrayQueue):
    """
    Double-Ended Queues implementation using Python list
    as unedrlying storage.

    [Michael T. Goodrich]The efficiency of an ArrayDeque is similar to
    that of an ArrayQueue, with all operations having O(1) running time,
    but with that bound being     amortized for operations that may change
    the size if the underlying list.
    """
    # moderate capacity for all new queues
    def __init__(self):
        super().__init__()

    def last(self):
        """
        Return the last element of deque.
        """
        back = (self._font + self._size - 1) % len(self._data)
        return self._data[back]

    def add_last(self, e):
        """
        Add element to the bacl of deque
        """
        self.enqueue(e)

    def delete_last(self):
        """
        Remove and return the last element from deque.
        """
        if self.is_empty():
            raise Empty('Dequeue is empty!')
        answer = self.last()
        back = (self._font + self._size - 1) % len(self._data)
        self._data[back] = None
        self._size -= 1
        # shrinks
        if 0 < self._size < len(self._data) // 4:
            self._resize(len(self._data) // 2)
        return answer

    def first(self):
        """
        Return the first element of deque;
        an error occurs if the deque is emppty.
        """
        return self._data[self._font]

    def add_first(self, e):
        """
        Add element to the front of deque.
        """
        if len(self._data) == self._size:
            self._resize(self._size * 2)
        self._font = (self._font - 1) % len(self._data)
        self._data[self._font] = e
        self._size += 1

    def delete_first(self):
        """
        Remove and return the first element from deque.
        """
        self.dequeue()


# Here we used the class only for the
# implementation of LinkedDeque
class _DoublyLinkedBase:
    """A base class providing a doubly linked list representation"""

    class _Node:
        """Lightweight, nonpublic class for storing a double linked node"""
        __slots__ = '_element', '_prev', '_next'

        def __init__(self, element, prev, next):
            self._element = element
            self._prev = prev
            self._next = next

    def __init__(self):
        """Create an empty list"""
        self._header = self._Node(None, None, None)
        self._tailer = self._Node(None, None, None)
        self._header._next = self._tailer
        self._tailer._prev = self._header
        self._size = 0

    def __Len__(self):
        """Return the number of elements in the list"""
        return self._size

    def is_empty(self):
        """Return true if the list is empty"""
        return self._size == 0

    def _insert_between(self, e, predecessor, successor):
        """Add element e between two existing nodes and return new node.
        With a leading underscore because we do not intend for it to provide
        a coherent public interface for gneral use.
        """
        newest = self._Node(e, predecessor, successor)
        predecessor._next = newest
        successor._prev = newest
        self._size += 1
        return newest

    def _delete_node(self, node):
        """Delete nonsentinel node from the list and return its element"""
        predecessor = node._prev
        successor = node._next
        predecessor._next = successor
        successor._prev = predecessor
        self._size -= 1
        element = node._element
        node._prev = node._next = node._element = None
        return element


class LinkedDeque(_DoublyLinkedBase):
    """Double-ended queue implementation based on a doubly linked list

    All the operation with time complexity O(1)
    """

    def first(self):
        """Return(but not remove) the element at the front of the queue
        """
        if self.is_empty():
            raise Empty("Deque is empty!")
        return self._header._next._element

    def last(self):
        """Return(but not remove) the element at the back of the deque
        """
        if self.is_empty():
            raise Empty("Deque is empty!")
        return self._tailer._prev._element

    def insert_first(self, e):
        """Add an element to the front of the deque
        """
        self._insert_between(e, self._header, self._header._next)

    def insert_last(self, e):
        """Add an element to the back if the deque"""
        self._insert_between(e, self._tailer._prev, self._tailer)

    def delete_first(self):
        """Remove and return the element from the front of the deque
        Raise Empty exception if the deque is empty.
        """
        if self.is_empty():
            raise Empty("Deque is empty!")
        return self._delete_node(self._header._next)

    def delete_last(self):
        """Remove and return the element from the back of the deque
        Raise Empty exception if the deque is empty.
        """
        if self.is_empty():
            raise Empty("Deque is empty!")
        return self._delete_node(self._tailer._prev)
