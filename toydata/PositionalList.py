class _DoublyLinkedBase:
    """A base class providing a doubly linked list representation"""

    class _Node:
        """Lightweight, nonpublic class for storing a doubly linked node"""
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

    def __len__(self):
        """Return the number of element in the list"""
        return self._size

    def is_empty(self):
        """Return True if the list is empty"""
        return self._size == 0

    def _insert_between(self, e, predecessor, successor):
        """Add element e between two existing nodes and return  new node"""
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
        # record deleted element
        element = node._element
        # deprecate node
        node._prev = node._next = node._element = None
        return element


class PositionalList(_DoublyLinkedBase):
    """A sequential container of elements allowing positional access"""

    # Nested class
    class Position:
        """A abstraction representing the location of a single element"""

        def __init__(self, container, node):
            """Construct should not be invoked by user"""
            self._container = container
            self._node = node

        def element(self):
            """Return the element store at this Position"""
            return self._node._element

        def __eq__(self, other):
            """Return True if other is a Position representing the same
            location"""
            return type(self) is type(other) and other._node is self._node

        def __ne__(self, other):
            """Return True if other does not represent the same location"""
            return not (self == other)

    # utility method
    def _validate(self, p):
        """Return position's node, or raise appropriate error if invalid"""
        if not isinstance(p, self.Position):
            raise TypeError('P must be proper Position type')
        if p._container is not self:
            raise ValueError('p does not belong to this container')
        # convention for depreated nodes
        if p._node._next is None:
            raise ValueError('p is no longer valid')
        return p._node

    def _make_position(self, node):
        """Return Position instance for given nodee(or None if sentinel)"""
        # boundary violation
        if node is self._header or node is self._tailer:
            return None
        # legitimate position
        else:
            return self.Position(self, node)

    # Accessors
    def first(self):
        """Return the first Position in the list(or None if list is empty)"""
        return self._make_position(self._header._next)

    def last(self):
        """Return the last Position in the list(or None if list is empty)"""
        return self._make_position(self._tailer._prev)

    def before(self, p):
        """Return the Position just before Position p
        (or None if p is first)"""
        node = self._validate(p)
        return self._make_position(node._prev)

    def after(self, p):
        """Return the Position just after Position p
        (or None if p is last)"""
        node = self._validate(p)
        return self._make_position(node._next)

    def __iter__(self):
        """Generate a forward iteration of the elements of the list"""
        cursor = self.first()
        while cursor is not None:
            yield cursor.element()
            cursor = self.after(cursor)

    # mutators
    def _insert_between(self, e, predecessor, successor):
        """Add element between exsiting nodes and return new Position"""
        node = super()._insert_between(e, predecessor, successor)
        return self._make_position(node)

    def add_first(self, e):
        """Insert element e at the front of the list and return new Pos"""
        return self._insert_between(e, self._header, self._header._next)

    def add_last(self, e):
        """Insert element e at the back of the list and return new Pos"""
        return self._insert_between(e, self._tailer._prev, self._tailer)

    def add_before(self, p, e):
        """Insert element e into list before Position p and return new Pos"""
        original = self._validate(p)
        return self._insert_between(e, original._prev, original)

    def add_after(self, p, e):
        """Insert element e into list after Position p and return new Pos"""
        original = self._validate(p)
        return self._insert_between(e, original, original._next)

    def delete(self, p):
        """Remove and return the element at Position p"""
        original = self._validate(p)
        return self._delete_node(original)

    def replace(self, p, e):
        """Replace the element at Position p with e.
        Return the element formerly at Position p"""
        original = self._validate(p)
        old_value = original._element
        original._element = e
        return old_value
