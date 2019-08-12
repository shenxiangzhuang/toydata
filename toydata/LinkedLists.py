from toydata.utils import Empty
from typing import Optional


class Node:
    """
    Node in Single linked list.
    """
    def __init__(self, value):
        self.value = value
        self.next: Optional['Node'] = None

    def __str__(self):
        """Show the node in single linked list properly"""
        return f"Node({self.value})"


class Singlellist:
    """
    The implementation of single linked list.
    """

    def __init__(self, items=None):
        self.head = None
        self.tail = None
        self.size = 0
        if items:
            for item in items:
                self.add_last(item)

    def __len__(self):
        """The length of the list.

        Time complexity: O(1)
        """
        return self.size

    def __str__(self):
        """Show the list properly.

        Time complexity: O(n)
        """
        items = []
        pointer = self.head
        while pointer is not None:
            items.append(pointer.value)
            pointer = pointer.next
        return f"SLL{items}"

    def __contains__(self, value):
        """
        Check if there is a value in the list, support for `in`

        Time complexity: O(n)
        """
        points = self.head
        while points is not None:
            if points.value == value:
                return True
            points = points.next
        return False

    def __getitem__(self, index):
        """Get the element by index, sll[index]

        Time complexity: O(n)
        """
        assert 0 <= index <= (len(self) - 1), "Index out of range"
        p = self.head
        while index > 0:
            p = p.next
            index -= 1
        return p.value

    def __setitem__(self, index, val):
        """Set the element by index, sll[index]=val

        Time complexity: O(n)
        """
        assert 0 <= index <= (len(self) - 1), "Index out of range"
        p = self.head
        while index > 0:
            p = p.next
            index -= 1
        p.value = val

    def is_empty(self):
        """If the list is empty or not

        Time complexity: O(1)
        """
        return self.size == 0

    def add_first(self, value):
        """
        Inserting an element at the head of a single linked list

        Time complexity: O(1)
        """
        new_node = Node(value)
        # empty list
        if self.is_empty():
            self.head = new_node
            self.tail = new_node
        else:
            new_node.next = self.head
            self.head = new_node
        self.size += 1

    def add_last(self, value):
        """
        Adding element at the end of single linked list

        Time complexity: O(1)
        """
        new_node = Node(value)
        # empty list
        if self.is_empty():
            self.head = new_node
            self.tail = new_node
        else:
            self.tail.next = new_node
            self.tail = new_node
        self.size += 1

    def insert_after(self, pos_value, insert_value):
        """
        Insert the insert_value after the (first)pos_value

        Time complexity: O(n)
        """
        assert pos_value in self, f"There is no {pos_value} in list"
        insert_node = Node(insert_value)
        pointer = self.head
        while pointer.value != pos_value:
            pointer = pointer.next
        insert_node.next = pointer.next
        pointer.next = insert_node
        self.size += 1

    def remove_first(self):
        """
        Remove the first element in the single linked list.
        Or raise an empty error when there is no node in the list.

        Time complexity: O(1)
        """
        if self.is_empty():
            raise Empty("The single linked list is empty")
        answer = self.head
        self.head = self.head.next
        self.size -= 1
        return answer

    def remove_last(self):
        """
        Remove the last element in the single linked list.
        Or raise an empty error when there is no node in the list.

        Time complexity: O(n)
        """
        if self.is_empty():
            raise Empty("The single linked list is empty")
        answer = self.tail
        # when head = tail, we should change head too.
        if self.size == 1:
            self.head = None
            self.tail = None
        else:
            pointer = self.head
            while pointer.next != self.tail:
                pointer = pointer.next
            self.tail = pointer
            self.tail.next = None
        self.size -= 1
        return answer

    def remove(self, val):
        """
        Remove the first node with value equals to val.

        Time complexity: O(n)
        """
        assert val in self, f"{val} don't in list!"
        p = self.head
        # val in the head of the list
        if p.value == val:
            self.remove_first()
        else:
            while p.next.value != val:
                p = p.next
            # val in the end of the list
            if p.next.next is None:
                self.tail = p
            p.next = p.next.next
            self.size -= 1

    def remove_all(self, val):
        """
        Remove all the node woth value = val

        Note that we can do it in O(n), but we used an efficient
        algorithm here.
        """
        while val in self:
            self.remove(val)

    def change(self, old_val, new_val):
        """
        Change the first node with value "old_val" to "new_val"

        Time complexity: O(n)
        """
        assert old_val in self, f"{old_val} not in list!"
        p = self.head
        while p.value != old_val:
            p = p.next
        p.value = new_val

    def change_all(self, old_val, new_val):
        """
        Change all the node with "old_val" to "new_val"

        Note that we can do it in O(n), but we used an efficient
        algorithm here.
        """
        while old_val in self:
            self.change(old_val, new_val)

    def search(self, value):
        """
        If value in list or not.

        Time complexity: O(n)
        """
        return value in self


class Doublellist:
    """Double linked list(with sentinels)"""

    class _Node:
        """Lightweight, nonpublic class for storing a
        doubly linked node."""
        # streamline memory
        __slots__ = '_element', '_prev', '_next'

        def __init__(self, element, prev, next):
            """Create a Node"""
            self._element = element
            self._prev = prev
            self._next = next

        def __str__(self):
            """Show the node in double linked list properly."""
            return f"{self._element}"

    def __init__(self, items=None):
        """Create a empty list"""
        self._header = self._Node(None, None, None)
        self._tailer = self._Node(None, None, None)
        self._size = 0
        # note that we must link the header and tailer firstly
        self._header._next = self._tailer
        self._tailer._prev = self._header
        if items:
            for item in items:
                self.add_last(item)

    def is_empty(self):
        """If the list is empty or not

        Time complexity: O(1)
        """
        return self._size == 0

    def __len__(self):
        """Return the size of the list

        Time complexity: O(1)
        """
        return self._size

    def __str__(self):
        """Show the double linked list properly.

        Time complexity: O(n)
        """
        result = ''
        result += 'Header'
        if not self.is_empty():
            ptr = self._header._next
            while ptr._element is not None:
                result += '->' + str(ptr)
                ptr = ptr._next
        result += '->Tailer'
        return result

    def __contains__(self, val):
        """If val in list or not

        Time complexity: O(n)
        """
        ptr = self._header
        i = self._size
        while i > 0:
            if ptr._next._element == val:
                return True
            ptr = ptr._next
            i -= 1
        return False

    def first(self):
        """Return the first value in the list.
        Or raise Empty error if the list is empty.

        Time complexity: O(1)
        """
        if self._size == 0:
            raise Empty('The list is empty!')
        return self._header._next._element

    def last(self):
        """Return the last value in the list.
        Or raise Empty error if the list is empty.

        Time complexity: O(1)
        """
        if self._size == 0:
            raise Empty('The list is empty!')
        return self._tailer._prev._element

    def add_first(self, e):
        """
        Add a node at the first of the list.

        Time complexity: O(1)
        """
        new_node = self._Node(e, self._header, self._header._next)
        self._header._next._prev = new_node
        self._header._next = new_node
        self._size += 1

    def add_last(self, e):
        """Add a node at the last of the list

        Time complexity: O(1)
        """
        new_node = self._Node(e, self._tailer._prev, self._tailer)
        self._tailer._prev._next = new_node
        self._tailer._prev = new_node
        self._size += 1

    def insert_after(self, pos_val, ins_val):
        """
        Insert `ins_val` after `pos_val`

        Time complexity: O(n)
        """
        # make sure there are a pos_val in list
        assert pos_val in self, f"{pos_val} not in list!"
        ptr = self._header
        while ptr._element != pos_val:
            ptr = ptr._next
        new_node = self._Node(ins_val, ptr, ptr._next)
        ptr._next._prev = new_node
        ptr._next = new_node
        self._size += 1

    def remove_first(self):
        """
        Remove the first node of the list.
        Or raise an Empty error if the list is empty.

        Time complexity: O(1)
        """
        if self.is_empty():
            raise Empty("The list is empty!")
        element = self.first()
        self._header._next._next._prev = self._header
        self._header._next = self._header._next._next
        self._size -= 1
        return element

    def remove_last(self):
        """Remove the last node of the list

        Time complexity: O(1)"""
        if self.is_empty():
            raise Empty("The list is empty!")
        element = self.first()
        self._tailer._prev._prev = self._tailer
        self._tailer._prev = self._tailer._prev._prev
        self._size -= 1
        return element

    def remove(self, val):
        """
        Only remove the first node with value equals `val`

        Time complexity: O(n)
        """
        assert val in self, f"{val} not in list!"
        ptr = self._header
        while ptr._next._element != val:
            ptr = ptr._next
        ptr._next._next._prev = ptr
        ptr._next = ptr._next._next
        self._size -= 1

    def remove_all(self, val):
        """
        Remove all the nodes with value equals `val`

        Note: here we use an efficient way to do that
        """
        while val in self:
            self.remove(val)

    def change(self, old_val, new_val):
        """
        Only change the first node with `old_val` to `new_val`

        Time complexity: O(n)
        """
        ptr = self._header
        while ptr._next._element != old_val:
            ptr = ptr._next
        ptr._next._element = new_val

    def change_all(self, old_val, new_val):
        """
        Change all the node with `old_val` to `new_val`

        Note: here we use an efficient way to do that
        """
        while old_val in self:
            self.change(old_val, new_val)

    def search(self, val):
        """If val in list of not

        Time complexity: O(n)
        """
        return val in self
