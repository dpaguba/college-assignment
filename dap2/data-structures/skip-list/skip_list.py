"""Skip list: a linked list with express lanes, balanced by coin flips.

A node is promoted to the next level with probability P. At 1/2 the expected
height is log2(n); at 1/4 the list is shorter and slightly slower, which is
what Redis uses.
"""

from __future__ import annotations

import random

PROMOTION = 0.5
MAX_LEVEL = 24

class Node:
    """One node: a key, its value, and a forward link per level it reaches."""
    __slots__ = ("key", "value", "forward")

    def __init__(self, key, value, level):
        """A node holding its own value and its links."""
        self.key = key
        self.value = value
        self.forward: list = [None] * level

class SkipList:
    """An ordered dictionary that gets its balance from randomness.

    A sorted linked list needs n steps to find anything, because there is no
    way to skip. A skip list adds express lanes above it: every node appears
    on level 0, half of them on level 1, a quarter on level 2, and so on. A
    search runs along the highest lane until the next node overshoots, drops a
    level, and repeats, so it covers the list in log n steps.

    The levels are decided by coin flips at insertion time, not by any rule
    about the data. There is no rebalancing, no rotation, no case analysis:
    the expected shape is good regardless of insertion order, and the bad case
    needs a run of bad luck rather than a bad input. That is the whole appeal.
    Pugh's 1990 paper argues it purely on how much simpler it is to implement
    correctly than a balanced tree, and anyone who has written red-black delete
    agrees.

    Concurrency is the other reason it survives: an insert touches a handful of
    pointers with no rotations, so lock-free versions are practical. Redis uses
    one for sorted sets, LevelDB for its memtable.
    """

    def __init__(self, promotion=PROMOTION, seed=None):
        """An empty list with the given promotion probability."""
        self._head = Node(None, None, MAX_LEVEL)
        self._level = 1
        self._count = 0
        self._promotion = promotion
        self._random = random.Random(seed)

    def _random_level(self):
        """The level of a new node, drawn from the promotion probability."""
        level = 1
        while self._random.random() < self._promotion and level < MAX_LEVEL:
            level += 1
        return level

    def _path_to(self, key):
        """The last node on each level that comes before `key`."""
        update = [self._head] * MAX_LEVEL
        node = self._head
        for level in range(self._level - 1, -1, -1):
            while node.forward[level] is not None and node.forward[level].key < key:
                node = node.forward[level]
            update[level] = node
        return update, node.forward[0]

    def insert(self, key, value=None):
        """Store a value under a key, promoting the new node by coin flips.

        O(log n) expected, with no rotations and no rebalancing code at all.
        """
        update, candidate = self._path_to(key)
        if candidate is not None and candidate.key == key:
            candidate.value = value
            return

        level = self._random_level()
        self._level = max(self._level, level)
        fresh = Node(key, value, level)
        for index in range(level):
            fresh.forward[index] = update[index].forward[index]
            update[index].forward[index] = fresh
        self._count += 1

    def search(self, key):
        """Value stored under the key, or None. O(log n) expected."""
        _, candidate = self._path_to(key)
        return candidate.value if candidate is not None and candidate.key == key else None

    def delete(self, key):
        """Remove a key by unlinking it from every level it appears on."""
        update, candidate = self._path_to(key)
        if candidate is None or candidate.key != key:
            return False

        for index in range(self._level):
            if update[index].forward[index] is not candidate:
                break
            update[index].forward[index] = candidate.forward[index]

        while self._level > 1 and self._head.forward[self._level - 1] is None:
            self._level -= 1
        self._count -= 1
        return True

    def items(self):
        """Every pair in ascending key order, by walking the bottom level."""
        node = self._head.forward[0]
        while node is not None:
            yield node.key, node.value
            node = node.forward[0]

    def keys(self):
        """Every key in ascending order."""
        for key, _ in self.items():
            yield key

    def height(self):
        """How many levels the list currently has."""
        return self._level

    def __contains__(self, key):
        """Whether the key is stored."""
        _, candidate = self._path_to(key)
        return candidate is not None and candidate.key == key

    def __len__(self):
        """How many entries the structure holds."""
        return self._count
