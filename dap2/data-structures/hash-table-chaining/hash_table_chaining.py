"""Hash table with separate chaining: a bucket per hash, a list per bucket.

The table grows at a load factor of 0.75. Above that the chains get long enough
that lookups start to feel linear.
"""

from __future__ import annotations

MAX_LOAD = 0.75
INITIAL_CAPACITY = 8

class HashTableChaining:
    """A dictionary that answers in constant time on average.

    The hash function turns a key into a bucket index, so a lookup goes
    straight to one bucket instead of searching. Two keys landing in the same
    bucket is a collision, and chaining handles it by keeping a list there.

    Average O(1) rests on two conditions. The hash must spread keys evenly:
    a bad one puts everything in one bucket and every operation becomes O(n),
    which is the worst case and the reason hash flooding is an attack. And the
    load factor must stay bounded, which is what the resize below enforces.

    Resizing rehashes everything, so one insert in n costs O(n). Amortised
    over the inserts that did not resize, it is still constant.
    """

    def __init__(self, capacity=INITIAL_CAPACITY):
        """An empty table of the given capacity."""
        self._buckets: list[list[tuple]] = [[] for _ in range(capacity)]
        self._count = 0

    def _index(self, key):
        """The bucket a key belongs to."""
        return hash(key) % len(self._buckets)

    def _grow(self):
        """Doubles the table and reinserts everything into it."""
        old = self._buckets
        self._buckets = [[] for _ in range(len(old) * 2)]
        self._count = 0
        for bucket in old:
            for key, value in bucket:
                self.insert(key, value)

    def insert(self, key, value=None):
        """Store a value under a key, growing the table when it passes the load factor.

        O(1) expected.
        """
        bucket = self._buckets[self._index(key)]
        for position, (existing, _) in enumerate(bucket):
            if existing == key:
                bucket[position] = (key, value)
                return
        bucket.append((key, value))
        self._count += 1
        if self._count / len(self._buckets) > MAX_LOAD:
            self._grow()

    def search(self, key):
        """Value stored under the key, or None.

        O(1) expected, O(n) if every key collides.
        """
        for existing, value in self._buckets[self._index(key)]:
            if existing == key:
                return value
        return None

    def delete(self, key):
        """Remove a key from its chain. O(1) expected."""
        bucket = self._buckets[self._index(key)]
        for position, (existing, _) in enumerate(bucket):
            if existing == key:
                del bucket[position]
                self._count -= 1
                return True
        return False

    def keys(self):
        """Every key, in no particular order."""
        for bucket in self._buckets:
            for key, _ in bucket:
                yield key

    def items(self):
        """Every pair, in no particular order."""
        for bucket in self._buckets:
            yield from bucket

    def __contains__(self, key):
        """Whether the key is stored."""
        return any(existing == key for existing, _ in self._buckets[self._index(key)])

    def __len__(self):
        """How many entries the structure holds."""
        return self._count
