"""Bloom filter: says "definitely not" or "probably", and never stores the data."""

from __future__ import annotations

import hashlib
from math import ceil, exp, log

class BloomFilter:
    """A set that trades certainty for memory, and gets orders of magnitude.

    Every other structure here can tell you exactly what it holds, because it
    holds it. A Bloom filter holds nothing: k hash functions map an item to k
    bit positions, and adding it sets those bits. Asking whether an item is
    present checks the same bits.

    That gives an asymmetry which is the whole point. If any bit is clear the
    item was definitely never added, so a negative answer is certain. If all
    are set the item is probably present, but the bits may have been set by
    other items, so a positive answer can be wrong. **False positives happen,
    false negatives cannot.**

    A million items at a one percent error rate cost about 1.2 MB, against
    tens of megabytes for a real set. That is why the pattern is everywhere
    something expensive sits behind a cheap check: databases skip disk reads
    for keys the filter denies, browsers screen URLs against malware lists,
    caches avoid a network call for objects they know are absent.

    Deletion is impossible: clearing a bit could erase an item that shares it.
    Counting Bloom filters replace bits with small counters to allow it.

    Both the bit count and the number of hash functions fall out of minimising
    the false positive rate for a given size.
    """

    def __init__(self, expected_items=1000, false_positive_rate=0.01):
        """A filter sized for the expected count and error rate."""
        if not 0 < false_positive_rate < 1:
            raise ValueError("the error rate has to sit strictly between 0 and 1")

        self._size = max(1, ceil(-expected_items * log(false_positive_rate) / log(2) ** 2))
        self._hashes = max(1, round(self._size / expected_items * log(2)))
        self._bits = bytearray(ceil(self._size / 8))
        self._count = 0

    def _positions(self, item):
        """k positions from two hashes, which is as good as k independent ones."""
        digest = hashlib.blake2b(repr(item).encode(), digest_size=16).digest()
        first = int.from_bytes(digest[:8], "big")
        second = int.from_bytes(digest[8:], "big") | 1
        for index in range(self._hashes):
            yield (first + index * second) % self._size

    def add(self, item):
        """Record an item by setting the bits its hashes point at.

        Nothing is stored, so nothing can be removed.
        """
        for position in self._positions(item):
            self._bits[position // 8] |= 1 << (position % 8)
        self._count += 1

    def estimated_false_positive_rate(self):
        """What the error rate has grown to, given how much has been added."""
        if self._count == 0:
            return 0.0
        filled = 1 - exp(-self._hashes * self._count / self._size)
        return filled ** self._hashes

    @property
    def bits(self):
        """How many bits the filter holds."""
        return self._size

    @property
    def hash_count(self):
        """How many hash functions each item is passed through."""
        return self._hashes

    def __contains__(self, item):
        """Whether the key is stored."""
        return all(
            self._bits[position // 8] & (1 << (position % 8))
            for position in self._positions(item)
        )

    def __len__(self):
        """How many items were added, which the filter has to be told, not asked."""
        return self._count
