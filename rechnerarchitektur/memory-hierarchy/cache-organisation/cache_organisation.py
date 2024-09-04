"""Cache organisation: how an address becomes a place in the cache.

An address splits into three fields. The **offset** picks a byte inside a
block, the **index** picks the set, and the **tag** is what is left and is
stored to check whether the block found is the one wanted.

The three parameters trade against each other. A larger block exploits spatial
locality and wastes bandwidth when locality is poor. More associativity removes
conflicts and costs comparators and hit time. A larger cache removes capacity
misses and is slower.
"""

from __future__ import annotations


class Cache:
    """A set-associative cache, counting hits and misses."""

    def __init__(self, size, block, associativity):
        """Derive the field widths from the three parameters."""
        self.size = size
        self.block = block
        self.associativity = associativity
        self.sets = size // (block * associativity)
        self.offset_bits = (block - 1).bit_length()
        self.index_bits = (self.sets - 1).bit_length() if self.sets > 1 else 0
        self.storage = [[] for _ in range(self.sets)]
        self.hits = 0
        self.misses = 0

    def index_of(self, address):
        """Which set an address maps to."""
        return (address // self.block) % self.sets

    def tag_of(self, address):
        """The part of the address that identifies the block within a set."""
        return address // (self.block * self.sets)

    def access(self, address):
        """Look an address up, inserting it on a miss. `True` on a hit."""
        index = self.index_of(address)
        tag = self.tag_of(address)
        entries = self.storage[index]

        if tag in entries:
            self.hits += 1
            return True

        self.misses += 1
        entries.append(tag)
        if len(entries) > self.associativity:
            entries.pop(0)
        return False

    def hit_rate(self):
        """Fraction of accesses that hit."""
        total = self.hits + self.misses
        return self.hits / total if total else 0.0


def miss_rate(cache, addresses):
    """Miss rate of an address stream on a fresh view of the cache."""
    for address in addresses:
        cache.access(address)
    total = cache.hits + cache.misses
    return cache.misses / total if total else 0.0


def address_fields(cache, address):
    """The three fields of an address, for the exercise's table."""
    return {
        "tag": cache.tag_of(address),
        "index": cache.index_of(address),
        "offset": address % cache.block,
    }


def blocks_per_set(cache):
    """Associativity, named as the exercise sheets name it."""
    return cache.associativity


def describe(cache):
    """The organisation as the numbers a specification would quote."""
    return {
        "size": cache.size,
        "block": cache.block,
        "sets": cache.sets,
        "ways": cache.associativity,
        "offset bits": cache.offset_bits,
        "index bits": cache.index_bits,
    }
