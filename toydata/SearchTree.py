from toydata.Maps import MapBase
from toydata.Tree import LinkedBinaryTree


class TreeMap(LinkedBinaryTree, MapBase):
    """Base class, Sorted map implementation using a binary search tree.
    
    Space complexity: O(n)
    Time complexity(Worst): 
    find_range: O(s + h)
    iter, reversed: O(n)
    others: O(h)
    h = the height of the tree(n when worst)
    """
    
    # override Position class
    class Position(LinkedBinaryTree.Position):
        def key(self):
            """Return key of maps's key-value pair"""
            return self.element()._key

        def value(self):
            """Return value of map's key-value pair"""
            return self.element()._value

    # nonpublic utilities
    def _subtree_search(self, p, k):
        """Return Position of p's subtree having key k, or last node
        searched"""
        # found match
        if k == p.key():
            return p
        # search left subtree
        if k < p.key():
            if self.left(p) is not None:
                return self._subtree_search(self.left(p), k)
        # search right subtree
        else:
            if self.right(p) is not None:
                return self._subtree_search(self.right(p), k)
        # unsuccessful search
        return p
    
    def _subtree_first_position(self, p):
        """Return Position if first item in subtree rooted at p"""
        walk = p
        # keep walking left
        while self.left(walk) is not None:
            walk = self.left(walk)
        return walk
    
    def _subtree_last_position(self, p):
        """Return Position of last item in subtree rooted at p"""
        walk = p
        # keep walking right
        while self.right(walk) is not None:
            walk = self.right(walk)
        return walk
    
    # Nonpublic Methods for Rotating and Restructuring
    def _relink(self, parent, child, make_left_child):
        """Relink parent node with child node
        (we allow child to be None)"""
        # make it a left child
        if make_left_child:
            parent._left = child
        else:
            parent._right = child
        # make child point to parent
        if child is not None:
            child._parent = parent

    def _rotate(self, p):
        """Rotate Position p above its parent"""
        x = p._node
        # we assume this exist
        y = x._parent
        # grandparent(possibly None)
        z = y._parent
        if z is None:
            # x becomes root
            self._root = x
            x._parent = None
        else:
            # x becomes a direct child of z
            self._relink(z, x, y == z._left)
        # now rotate x and y, including transfer of middle subtree
        if x == y._left:
            # x._right becomes left child of y
            self._relink(y, x._right, True)
            # y becomes right child of x
            self._relink(x, y, False)
        else:
            # x._left becomes right child of y
            self._relink(y, x._left, False)
            # y becomes left child of x
            self._relink(x, y, True)
    
    def _restructure(self, x):
        """Perform tirnode restructure of Position x with parent/grandparent"""
        y = self.parent(x)
        z = self.parent(y)
        if(x == self.right(y)) == (y == self.right(z)):
            # single rotation (of y)
            self._rotate(y)
            # y is new subtree root
            return y
        else:
            # double rotation (of x)
            self._rotate(x)
            self._rotate(x)
            # x is new subtree root
            return x

    # balanced tree subclassed
    def _rebalance_access(self, p):
        pass

    def _rebalance_insert(self, p):
        pass

    def _rebalance_delete(self, p):
        pass
    
    def first(self):
        """Return the first Position in the tree(or None if empty)"""
        if len(self) > 0:
            return self._subtree_first_position(self.root())
        else:
            return None
    
    def last(self):
        """Return the last Position in the etree(or None if empty)"""
        if len(self) > 0:
            return self._subtree_last_position(self.root())
        else:
            return None
    
    def before(self, p):
        """Return the Position just before p in the natural order.
        Return None if p is the first position.
        """
        # inheried from LinkedBinaryTree
        self._validate(p)
        if self.left(p):
            return self._subtree_last_position(self.left(p))
        else:
            # walk upward
            walk = p
            above = self.parent(walk)
            while above is not None and walk == self.left(above):
                walk = above
                above = self.parent(walk)
            return above
        
    def after(self, p):
        """Return the Position just after p in the natural order.
        Return None if p is the last position"""
        self._validate(p)
        if self.right(p):
            return self._subtree_first_position(self.right(p))
        else:
            # walk upward
            walk = p
            above = self.parent(walk)
            while above is not None and walk == self.right(above):
                walk = above
                above = self.parent(walk)
            return above

    def find_position(self, k):
        """Return position with key k, or else neighbor(or None if empty)"""
        if self.is_empty():
            return None
        else:
            p = self._subtree_search(self.root(), k)
            # hook for balance tree subclasses
            self._rebalance_access(p)
            return p
        
    def find_min(self):
        """Return (key, value) pair with minimum key(or None if empty)
        """
        if self.is_empty():
            return None
        p = self.first()
        # Note here we use `isinstance` to ensure p
        # is a position instance only which has key() and value()
        if isinstance(p, TreeMap.Position):
            return (p.key(), p.value())
    
    def find_ge(self, k):
        """Return (key, value) pair with least key greater than
        or equal to k. Return None if there does not exist such a key.
        """
        if self.is_empty():
            return None
        else:
            # may not find exact match
            p = self.find_position(k)
            # p's key is too small
            if isinstance(p, TreeMap.Position) and p.key() < k:
                    p = self.after(p)
            if isinstance(p, TreeMap.Position):
                return (p.key(), p.value())
            else:
                return None
        
    def find_range(self, start, stop):
        """Iterate all (key, value) pairs such that
        start <= key < stop.

        If start is None, iteration begins with minimum key of map..
        If stop is None, iteration continues throungh the maximum key
        of map"""

        if not self.is_empty():
            if start is None:
                p = self.first()
            else:
                # we initialize p with logic similar to find_ge
                p = self.find_position(start)
                if isinstance(p, TreeMap.Position) and p.key() < start:
                    p = self.after(p)
            while isinstance(p, TreeMap.Position) and \
                    (stop is None or p.key() < stop):
                yield (p.key(), p.value())
                p = self.after(p)
            
    def __getitem__(self, k):
        """Return value associated with key k
        (raise KeyError if not found)"""
        if self.is_empty():
            raise KeyError('Key Error: ' + repr(k))
        else:
            p = self._subtree_search(self.root(), k)
            self._rebalance_access(p)
            if isinstance(p, TreeMap.Position):
                if k != p.key():
                    raise KeyError('Key Error: ' + repr(k))
                return p.value()
    
    def __setitem__(self, k, v):
        """Assign value v to key k, overwriting exsiting value
        if present"""
        leaf = None
        if self.is_empty():
            # from LinkedBinaryTree
            leaf = self._add_root(self._Item(k, v))
        else:
            p = self._subtree_search(self.root(), k)
            if isinstance(p, TreeMap.Position):
                if p.key() == k:
                    # replace existing item's value
                    p.element()._value = v
                    self._rebalance_access(p)
                    return
                else:
                    item = self._Item(k, v)
                    if p.key() < k:
                        # inherited from LinkedBinaryTree
                        leaf = self._add_right(p, item)
                    else:
                        leaf = self._add_left(p, item)
        if leaf:
            self._rebalance_insert(leaf)

    def __iter__(self):
        """Generate an iteration of all keys in the map in order"""
        p = self.first()
        while isinstance(p, TreeMap.Position) and p is not None:
            yield p.key()
            p = self.after(p)

    def __len__(self):
        """Return the total number of elements in the tree

        Time complexity: O(1)
        """
        return self._size
    
    def delete(self, p):
        """Remove the item at given Position"""
        self._validate(p)
        if self.left(p) and self.right(p):
            replacement = self._subtree_last_position(self.left(p))
            self._replace(p, replacement.element())
            p = replacement
        # now p has at most one child
        parent = self.parent(p)
        self._delete(p)
        self._rebalance_delete(parent)

    def __delitem__(self, k):
        """remove item associated with key k
        (raise KeyError if not found)"""
        if not self.is_empty():
            p = self._subtree_search(self.root(), k)
            if isinstance(p, TreeMap.Position) and k == p.key():
                self.delete(p)
                return
            self._rebalance_access(p)
        raise KeyError('Key Error: ' + repr(k))


class AVLTreeMap(TreeMap):
    """Sorted map implementation using an AVL tree.
    
    Space complexity: O(n)
    Time complexity(Worst): 
    find_range: O(s + logn)
    others: O(logn)
    iter, reversed: O(n)
    in other word: AVL Tree can ensure h = logn
    """

    # nested _Node class
    class _Node(TreeMap._Node):
        """Node class fro AVL maintains height value for balanceing."""
        __slots__ = '_height'  # additional data member to store height

        def __init__(self, element, parent=None, left=None, right=None):
            super().__init__(element, parent, left, right)
            self._height = 0  # will be recomputed during balancing
        
        def left_height(self):
            return self._left._height if self._left is not None else 0
        
        def right_height(self):
            return self._right._height if self._right is not None else 0
        
    # positional-based utility methods
    def _recompute_height(self, p):
        if p is None:
            return
        else:
            p._node._height = 1 + max(p._node.left_height(), p._node.right_height())
    
    def _isbalanced(self, p):
        return abs(p._node.left_height() - p._node.right_height()) <= 1
    
    # parameter `favorleft` contols tiebreaker
    def _tall_child(self, p, favorleft=False):
        hl, hr = p._node.left_height(), p._node.right_height()
        if hl + (1 if favorleft else 0) > hr:
            return self.left(p)
        else:
            return self.right(p)
    
    def _tall_grandchild(self, p):
        child = self._tall_child(p)
        # if child is on left, favor left grandchild;else favor right
        alignment = (child == self.left(p))
        return self._tall_child(child, alignment)

    def _rebalance(self, p):
        while p is not None:
            # trivially 0 if new node
            old_height = p._node._height
            # imbalance detected
            if not self._isbalanced(p):
                # perform trinode restructuring, setting p to resulting root.
                # and recompute new local heights after the constructuring
                p = self._restructure(self._tall_grandchild(p))
                self._recompute_height(self.left(p))
                self._recompute_height(self.right(p))
            self._recompute_height(p)  # adjust for recent changes
            if p._node._height == old_height:  # has height changed?
                p = None   # no further changes needed
            else:
                p = self.parent(p)  # repeat with parent
    
    # override balancing hooks
    def _rebalance_insert(self, p):
        self._rebalance(p)

    def _rebalance_delete(self, p):
        self._rebalance(p)


class SplayTreeMap(TreeMap):
    """Sorted map implementation using a splay tree"""

    # splay operation
    def _splay(self, p):
        while p != self.root():
            parent = self.parent(p)
            grand = self.parent(parent)
            if grand is None:
                # zig case
                self._rotate(p)
            elif(parent == self.left(grand)) == (p == self.left(parent)):
                # zig-zig case
                self._rotate(parent)  # move PARENT up
                self._rotate(p)       # then move p up
            else:
                # zig-zag case
                self._rotate(p)       # move p up
                self._rotate(p)       # move p up again
        
    # override balancing hooks
    def _rebalance_insert(self, p):
        self._splay(p)

    def _rebalance_delete(self, p):
        self._splay(p)

    def _rebalance_access(self, p):
        self._splay(p)


class RedBlackTreeMap(TreeMap):
    """Sorted map implementation using a red-black tree"""
    class _Node(TreeMap._Node):
        """Node clas for red-black tree maintains bit that
        denote color"""
        # add additional data member to the Node class
        __slots__ = '_red'
    
        def __init__(self, element, parent=None, left=None, right=None):
            super().__init__(element, parent, left, right)
            # new node red by default
            self._red = True

    # positional-based utility methods
    # we consider a nonexistent child to be trivially black
    def _set_red(self, p):
        if p: p._node._red = True

    def _set_black(self, p):
        if p: p._node._red = False
    
    def _set_color(self, p, make_red):
        if p: p._node._red = make_red
    
    def _is_red(self, p):
        return p is not None and p._node._red

    def _is_red_leaf(self, p):
        return self.is_leaf(p) and self._is_red(p)

    def _get_red_child(self, p):
        """Return a red child of p (or None if no such child)"""
        for child in (self.left(p), self.right(p)):
            if self._is_red(child):
                return child
            return None

    # support for insertion
    def _rebalance_insert(self, p):
        self._resolve_red(p)  # new node is always red

    def _resolve_red(self, p):
        """Solve red confliction cased when insertion"""
        if self.is_root(p):
            self._set_black(p)
        else:
            parent = self.parent(p)
            # double red problem
            if self._is_red(parent):
                uncle = self.sibling(parent)
                # rotation and recolor
                if not self._is_red(uncle):
                    # do trinode restructuring
                    middle = self._restructure(p)
                    self._set_black(middle)
                    self._set_red(self.left(middle))
                    self._set_red(self.right(middle))
                # just recolor recursively
                else:
                    grand = self.parent(parent)
                    self._set_red(grand)
                    self._set_black(self.left(grand))
                    self._set_black(self.right(grand))
                    # recur at red grandparent
                    self._resolve_red(grand)

    # support for deletions
    def _rebalance_delete(self, p):
        if len(self) == 1:
            # special case: ensure that root is black
            self._set_black(self.root())
        elif p is not None:
            n = self.num_children(p)
            if n == 1:  # deficit exists unless child is red leaf
                c = next(self.children(p))
                if not self._is_red_leaf(c):
                    self._fix_deficit(p, c)
            elif n == 2:
                # removed black node with red child
                if self._is_red_leaf(self.left(p)):
                    self._set_black(self.left(p))
                else:
                    self._set_black(self.right(p))

    def _fix_deficit(self, z, y):
        """Resolve black deficit at z, where y is 
        the root of z's heaview subtree"""
        if not self._is_red(y):  # y is black; will apply case 1 or 2
            x = self._get_red_child(y)
            if x is not None:
                old_color = self._is_red(z)
                middle = self._restructure(x)
                self._set_color(middle, old_color)
                self._set_black(self.left(middle))
                self._set_black(self.right(middle))
            else:
                self._set_red(y)
                if self._is_red(z):
                    self._set_black(z)
                elif not self.is_root(z):
                    self._fix_deficit(self.parent(z), self.sibling(z))
        else:
            self._rotate(y)
            self._set_black(y)
            self._set_red(z)
            if z == self.right(y):
                self._fix_deficit(z, self.left(z))
            else:
                self._fix_deficit(z, self.right(z))
