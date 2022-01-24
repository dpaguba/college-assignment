"""Hash table with open addressing: collisions move to the next free slot.

Open addressing degrades sharply as it fills, far earlier than chaining, so
this table grows at half full rather than three quarters.
"""

from __future__ import annotations

MAX_LOAD = 0.5
INITIAL_CAPACITY = 8

class _Deleted:
    """A tombstone: this slot was used, so probing must not stop here."""

TOMBSTONE = _Deleted()

class HashTableOpenAddressing:
    """A dictionary that keeps everything in one flat array.

    Chaining stores collisions in a list hanging off the bucket. Open
    addressing has no lists: on a collision it probes forward for the next free
    slot. Everything lives in one contiguous array, so lookups touch one cache
    line instead of chasing pointers, which is why real implementations,
    Python's own dict included, use this shape.

    Deletion is the awkward part. Emptying a slot would break every probe
    sequence that passed through it, so a deleted slot gets a tombstone
    instead: probing continues past it, but an insert may reuse it. Tombstones
    accumulate, which is one more reason to rehash on growth.

    This uses quadratic probing, step i² instead of i, because linear probing
    makes occupied slots clump into runs, and each run makes the next collision
    more likely.
    """

    def __init__(self, capacity=INITIAL_CAPACITY):
        """An empty table of the given capacity."""
        self._slots: list = [None] * capacity
        self._count = 0

    def _probe(self, key):
        """Yield the slots to examine for this key, in order."""
        start = hash(key) % len(self._slots)
        for step in range(len(self._slots)):
            yield (start + step * step) % len(self._slots)

    def _grow(self):
        """Doubles the table and reinserts everything into it."""
        old = [slot for slot in self._slots if slot not in (None, TOMBSTONE)]
        self._slots = [None] * (len(self._slots) * 2)
        self._count = 0
        for key, value in old:
            self.insert(key, value)

    def insert(self, key, value=None):
        """Store a value under a key, probing for a free slot.

        Quadratic probing can fail to reach a free slot even when one exists,
        so a rehash is the way out rather than an error.
        """
        first_free = None
        for index in self._probe(key):
            slot = self._slots[index]
            if slot is None:
                self._slots[first_free if first_free is not None else index] = (key, value)
                self._count += 1
                break
            if slot is TOMBSTONE:
                if first_free is None:
                    first_free = index
                continue
            if slot[0] == key:
                self._slots[index] = (key, value)
                return
        else:
            self._grow()
            self.insert(key, value)
            return

        if self._count / len(self._slots) > MAX_LOAD:
            self._grow()

    def _find(self, key):
        """The node holding the key, or nothing when it is absent."""
        for index in self._probe(key):
            slot = self._slots[index]
            if slot is None:
                return None
            if slot is not TOMBSTONE and slot[0] == key:
                return index
        return None

    def search(self, key):
        """Value stored under the key, or None.

        The probe stops at a truly empty slot, never at a tombstone.
        """
        index = self._find(key)
        return None if index is None else self._slots[index][1]

    def delete(self, key):
        """Remove a key, leaving a tombstone.

        Clearing the slot outright would cut the probe sequence of every key
        that collided with it.
        """
        index = self._find(key)
        if index is None:
            return False
        self._slots[index] = TOMBSTONE
        self._count -= 1
        return True

    def keys(self):
        """Every key, in no particular order."""
        for slot in self._slots:
            if slot not in (None, TOMBSTONE):
                yield slot[0]

    def items(self):
        """Every pair, in no particular order."""
        for slot in self._slots:
            if slot not in (None, TOMBSTONE):
                yield slot

    def __contains__(self, key):
        """Whether the key is stored."""
        return self._find(key) is not None

    def __len__(self):
        """How many entries the structure holds."""
        return self._count
