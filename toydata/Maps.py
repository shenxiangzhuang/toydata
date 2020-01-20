from random import randrange
from abc import ABCMeta, abstractmethod
from collections.abc import MutableMapping


class MapBase(MutableMapping):
    """
    Our own abstract base class that incudes a nonpublic _Item class.
    """
    # nested _Item class
    class _Item:
        """
        Lightweight composite to store key-value pairs as map items.
        """
        __slots__ = '_key', '_value'

        def __init__(self, k, v):
            self._key = k
            self._value = v

        def __str__(self):
            return f'({self._key}:{self._value})'

        def __eq__(self, other):
            return self._key == other._key

        def __ne__(self, other):
            return not (self == other)

        def __lt__(self, other):
            return self._key < other._key


class UnsortedTableMap(MapBase):
    """
    Map implementation using an unsorted list.
    """
    def __init__(self):
        """Create an empty map."""
        self._table = []

    def __str__(self):
        if not self._table:
            return "Empty"
        s = ''
        for item in self._table:
            s += f'|{str(item)}|'.center(5)
            s += '\n'
        # remove the last '\n'
        s = s.rstrip()
        return s

    def __getitem__(self, k):
        """
        Return value associated with key k
        (raise KeyError if not found)
        """
        for item in self._table:
            if k == item._key:
                return item._value
            raise KeyError('Key Error: ' + repr(k))

    def __setitem__(self, k, v):
        """Assign value v to key k,
        overwriting existing value if present."""
        for item in self._table:
            if k == item._key:
                item._value = v
                return
        self._table.append(self._Item(k, v))

    def __delitem__(self, k):
        """
        Remove item associated with key k
        (raise KeyError if not found).
        """
        for j in range(len(self._table)):
            if k == self._table[j]._key:
                self._table.pop(j)
            return
        raise KeyError('Key Error: ' + repr(k))

    def __len__(self):
        """
        Return number of items in the map.
        """
        return len(self._table)

    def __iter__(self):
        """
        Generate iteration of the map's keys.
        """
        for item in self._table:
            yield (item._key, item._value)


class HashMapBase(MapBase, metaclass=ABCMeta):
    """
    Abstract base class for map using hash-table with MAD compression.
    """
    def __init__(self, cap=4, p=10945121):
        """Create an empty hash-table map."""
        self._table = cap * [None]
        # number of the entries in the map
        self._n = 0
        # prime for MAD compression
        self._prime = p
        # scale form 1 to p-1 for MAD
        self._scale = 1 + randrange(p - 1)
        # shift from 0 to p-1 for MAD
        self._shift = randrange(p)

    def _hash_function(self, k):
        return (hash(k) * self._scale + self._shift) \
            % self._prime % len(self._table)

    def __len__(self):
        return self._n

    @abstractmethod
    def _bucket_getitem(self, j, k):
        pass

    @abstractmethod
    def _bucket_setitem(self, j, k, v):
        pass

    @abstractmethod
    def _bucket_delitem(self, j, k):
        pass

    @abstractmethod
    def __iter__(self):
        pass

    @abstractmethod
    # resize bucket array to capcity c
    def _resize(self, c):
        pass

    def __getitem__(self, k):
        j = self._hash_function(k)
        return self._bucket_getitem(j, k)

    def __setitem__(self, k, v):
        j = self._hash_function(k)
        self._bucket_setitem(j, k, v)
        if self._n > len(self._table) // 2:
            # number 2*x-1 is often prime
            self._resize(2 * len(self._table) - 1)

    def __delitem__(self, k):
        j = self._hash_function(k)
        self._bucket_delitem(j, k)
        self._n -= 1


class ChainHashMap(HashMapBase):
    """Hash map implemented with seperate chaining for collision resolution"""

    def __str__(self):
        N = len(self._table)
        s = ''
        for i in range(N):
            s += ('|' + f'  {i}  ' + '|')
        s += '\n'
        s += '   |   ' * N + '\n'
        s += '   v   ' * N + '\n'
        for i in range(N):
            if self._table[i] is None:
                s += 'None'.center(7)
            else:
                s += str(self._table[i]).replace('\n',
                                                 '\n' + ' ' * i * 7)

        return s

    def _bucket_getitem(self, j, k):
        bucket = self._table[j]
        if bucket is None:
            raise KeyError("Key Error: " + repr(k))
        return bucket[k]

    def _bucket_setitem(self, j, k, v):
        if self._table[j] is None:
            # bucket is new to the table
            self._table[j] = UnsortedTableMap()
        oldsize = len(self._table[j])
        self._table[j][k] = v
        if len(self._table[j]) > oldsize:
            self._n += 1

    def _bucket_delitem(self, j, k):
        bucket = self._table[j]
        if bucket is None:
            raise KeyError("Key Error: " + repr(k))
        del bucket[k]

    def __iter__(self):
        for bucket in self._table:
            if bucket is not None:
                for key in list(bucket):
                    yield key

    # resize bucket array to capcity c
    def _resize(self, c):
        unsort_maps = [unsort_map for unsort_map in self._table if unsort_map]
        old = []
        for unsort_map in unsort_maps:
            for item in unsort_map:
                old.append(item)
        self._table = c * [None]
        self._n = 0
        for (k, v) in old:
            self[k] = v


class ProbeHashMap(HashMapBase):
    """
    Hash map implementated with linear probing for collision resolution.
    """
    # sentinal marks locations of previous deletion
    _AVAIL = object()

    def __str__(self):
        N = len(self._table)
        s = ''
        for i in range(N):
            s += ('|' + f'  {str(self._table[i])}  ' + '|')
        return s

    def _is_available(self, j):
        """Return True if index j is available in table."""
        return self._table[j] is None or self._table[j] is ProbeHashMap._AVAIL

    def _find_slot(self, j, k):
        """
        Search for key k in bucket at index j.

        Return (success, index) tuple, decribed as follows:
        if match was found, success is True and index denotes its location.
        if no match  found, success is False and index denotes first available
        slot.
        """
        firstAvail = None
        while True:
            if self._is_available(j):
                if firstAvail is None:
                    firstAvail = j
                if self._table[j] is None:
                    return (False, firstAvail)
            elif k == self._table[j]._key:
                return (True, j)
            j = (j + 1) % len(self._table)

    def _bucket_getitem(self, j, k):
        found, s = self._find_slot(j, k)
        if not found:
            raise KeyError('Key Error: ' + repr(k))
        return self._table[s]._value

    def _bucket_setitem(self, j, k, v):
        found, s = self._find_slot(j, k)
        if not found:
            self._table[s] = self._Item(k, v)
            self._n += 1
        else:
            self._table[s]._value = v

    def _bucket_delitem(self, j, k):
        found, s = self._find_slot(j, k)
        if not found:
            raise KeyError('Key Error: ' + repr(k))
        self._table[s] = ProbeHashMap._AVAIL

    def __iter__(self):
        for j in range(self._table):
            if not self._is_available(j):
                yield self._table[j]._key

    # resize bucket array to capcity c
    def _resize(self, c):
        old = [item for item in self._table if item]
        self._table = c * [None]
        self._n = 0
        for item in old:
            self[item._key] = item._value


class SortedTableMap(MapBase):
    """Map implementation using a sorted table"""

    # nonpublic behaviors
    def _find_index(self, k, low, high):
        """Return index of the leftmost item with key greate
        than or equal to k.

        Return high + 1 if no such item qualifies.

        That is, j will be returned such that:
            all items of slice table[low:j] have key < k
            all items of slice table[j:high+1] have key >= k
        """
        if high < low:
            return high + 1
        else:
            mid = (low + high) // 2
            if k == self._table[mid]._key:
                return mid
            elif k < self._table[mid]._key:
                return self._find_index(k, low, mid - 1)
            else:
                return self._find_index(k, mid + 1, high)
    # public behaviors
    def __init__(self):
        """Create an empty map"""
        self._table = []
    
    def __str__(self):
        return ' '.join(str(item) for item in self._table)

    def __len__(self):
        """Return number of items in the map"""
        return len(self._table)
    
    def __getitem__(self, k):
        """Return value associated with kay k
        (raise KeyError if not found)"""
        j = self._find_index(k, 0, len(self._table) - 1)
        if j == len(self._table) or self._table[j]._key != k:
            raise KeyError('Key Errpr' + repr(k))
        return self._table[j]._value

    def __setitem__(self, k, v):
        """Assign value v to key k, overwriting existing value if present"""
        j = self._find_index(k, 0, len(self._table)-1)
        if j < len(self._table) and self._table[j]._key == k:
            self._table[j]._value = v
        else:
            self._table.insert(j, self._Item(k, v))

    def __delitem__(self, k):
        """Remove item associated with key k
        (raise KeyError if not found)
        """
        j = self._find_index(k, 0, len(self._table) - 1)
        if j == len(self._table) or self._table[j]._key != k:
            raise KeyError("Key Error: " + repr(k))
        self._table.pop(j)
    
    def __iter__(self):
        """Generate keys of the map ordered from minimum to maximum"""
        for item in self._table:
            yield item._key
        
    def __reversed__(self):
        """Generate keys of the map ordered from maximum to minimum"""
        for item in reversed(self._table):
            yield item._key
        
    def find_min(self):
        """Return (key, value) pair with minimum key(or None if empty)"""
        if len(self._table) > 0:
            return (self._table[0]._key, self._table[0]._value)
        else:
            return None
    
    def find_max(self):
        """Return (key, value) pair with maximum key(or None if empty)"""
        if len(self._table) > 0:
            return (self._table[-1]._key, self._table[-1]._value)
        else:
            return None

    def find_ge(self, k):
        """Return (key, value) pair with least key greater that or
        equal to k"""
        j = self._find_index(k, 0, len(self._table) - 1)
        if j < len(self._table):
            return (self._table[j]._key, self._table[j]._value)
        else:
            return None
        
    def find_lt(self, k):
        """Return (key, value) pair with greatest key strictly less than k"""
        j = self._find_index(k, 0, len(self._table) - 1)
        if j >= 0:
            return (self._table[j-1]._key, self._table[j-1]._value)
        else:
            return None
    
    def find_gt(self, k):
        """Return (key, value) pair with least key strictly greater than k"""
        # j's ley >= k
        j = self._find_index(k, 0, len(self._table) - 1)
        if j < len(self._table) and self._table[j]._key == k:
            j += 1    # advanced past match
        if j < len(self._table):
            return (self._table[j]._key, self._table[j]._value)
        else:
            return None

    def find_range(self, start, stop):
        """Iterate all (key, value) pairs such that start <= key < stop.
        If start is None, iteration begins with minimum key of map.
        If stop is None, iteration continues through the maximum key of map.
        """
        if start is None:
            j = 0
        else:
            # find first result
            j = self._find_index(start, 0, len(self._table) - 1)
        while j < len(self._table) and (stop is None or self._table[j]._key < stop):
            yield (self._table[j]._key, self._table[j]._value)
            j += 1
