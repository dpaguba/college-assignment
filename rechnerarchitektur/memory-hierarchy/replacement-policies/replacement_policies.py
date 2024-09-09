"""Replacement policies, and the anomaly one of them has.

When a set is full, something must go. Which one is a prediction about the
future made from the past, and the policies differ in how much past they use.

LRU is a **stack algorithm**: the contents of a cache with `n` ways are always a
subset of the contents of one with `n+1` ways, so more capacity can never cause
more misses. FIFO is not, and Belady's anomaly is the consequence: a larger
cache can miss more often, which is measured here rather than asserted.
"""

from __future__ import annotations


class Cache:
    """A set-associative cache with a choice of replacement policy."""

    def __init__(self, size, block, associativity, policy="lru"):
        """Set up the sets and the bookkeeping the policy needs."""
        self.size = size
        self.block = block
        self.associativity = associativity
        self.policy = policy
        self.sets = max(1, size // (block * associativity))
        self.storage = [[] for _ in range(self.sets)]
        self.hits = 0
        self.misses = 0
        self.clock = 0

    def access(self, address):
        """Look an address up, replacing by the policy on a miss."""
        self.clock += 1
        index = (address // self.block) % self.sets
        tag = address // (self.block * self.sets)
        entries = self.storage[index]

        for entry in entries:
            if entry["tag"] == tag:
                self.hits += 1
                if self.policy == "lru":
                    entry["used"] = self.clock
                return True

        self.misses += 1
        if len(entries) >= self.associativity:
            if self.policy == "lru":
                victim = min(entries, key=lambda entry: entry["used"])
            else:
                victim = min(entries, key=lambda entry: entry["inserted"])
            entries.remove(victim)

        entries.append({"tag": tag, "inserted": self.clock, "used": self.clock})
        return False


def miss_rate(cache, addresses):
    """Miss rate of an address stream."""
    for address in addresses:
        cache.access(address)
    total = cache.hits + cache.misses
    return cache.misses / total if total else 0.0


def optimal_miss_rate(addresses, size, block, associativity):
    """Belady's optimal policy: evict what is needed furthest in the future.

    Unimplementable, because it needs the future, and useful precisely for
    that: it is the lower bound every real policy is measured against. A policy
    close to it has little left to gain from being cleverer.
    """
    sets = max(1, size // (block * associativity))
    storage = [[] for _ in range(sets)]
    misses = 0

    for position, address in enumerate(addresses):
        index = (address // block) % sets
        tag = address // (block * sets)
        entries = storage[index]

        if tag in entries:
            continue

        misses += 1
        if len(entries) >= associativity:
            victim = _furthest_use(entries, addresses[position + 1:], block, sets, index)
            entries.remove(victim)
        entries.append(tag)

    return misses / len(addresses) if addresses else 0.0


def _furthest_use(entries, future, block, sets, index):
    """The cached block whose next use is furthest away, or never."""
    best = entries[0]
    best_distance = -1

    for entry in entries:
        distance = len(future) + 1
        for offset, address in enumerate(future):
            if (address // block) % sets != index:
                continue
            if address // (block * sets) == entry:
                distance = offset
                break
        if distance > best_distance:
            best, best_distance = entry, distance

    return best


def is_stack_algorithm(policy, stream, block, associativity_range):
    """Whether more capacity never increases the misses, for one stream.

    The definition of a stack algorithm, checked empirically. LRU satisfies it
    and FIFO does not, and the counterexample is Belady's anomaly.
    """
    previous = None

    for ways in associativity_range:
        cache = Cache(block * ways, block, ways, policy)
        rate = miss_rate(cache, stream)
        if previous is not None and rate > previous:
            return False
        previous = rate

    return True
