"""The branch target buffer: knowing *where* a taken branch goes.

A direction predictor says whether a branch is taken. It does not say where to
fetch from, and computing the target needs the instruction decoded, which is
one or more cycles after the fetch that needs it.

A branch target buffer caches the target address, indexed by the branch's own
address, so a hit lets the very next fetch go to the right place. The cost of a
miss is smaller than a misprediction, because the pipeline only stalls until
the target is known rather than discarding wrong work.
"""

from __future__ import annotations


class BranchTargetBuffer:
    """A direct-mapped cache from branch address to target address."""

    def __init__(self, entries):
        """Allocate the entries, each holding a tag and a target."""
        self.entries = entries
        self.tags = [None] * entries
        self.targets = [None] * entries
        self.hits = 0
        self.misses = 0

    def _index(self, address):
        """Which entry an address maps to."""
        return (address >> 2) % self.entries

    def lookup(self, address):
        """The recorded target, or `None` on a miss."""
        index = self._index(address)
        if self.tags[index] == address:
            self.hits += 1
            return self.targets[index]
        self.misses += 1
        return None

    def update(self, address, target):
        """Record a branch's target, evicting whatever shared the entry.

        Direct-mapped, so two branches that map to the same entry evict each
        other on every execution. That is why a loop containing two branches
        can perform worse than one containing three, and why real buffers are
        set associative.
        """
        index = self._index(address)
        self.tags[index] = address
        self.targets[index] = target

    def hit_rate(self):
        """Fraction of lookups that found a target."""
        total = self.hits + self.misses
        return self.hits / total if total else 0.0


def average_penalty(hit_rate, accuracy, miss_penalty, misprediction_penalty):
    """Expected cycles lost per branch, from both failure modes.

    A buffer miss costs the smaller penalty, because the target is merely late.
    A buffer hit with a wrong direction costs the larger one, because work was
    done and must be thrown away. The two are weighted by how often each
    happens, which is why improving direction accuracy matters more once the
    buffer hit rate is high.
    """
    return ((1 - hit_rate) * miss_penalty
            + hit_rate * (1 - accuracy) * misprediction_penalty)


def simulate(addresses, targets, entries):
    """Run a branch address stream through a buffer, reporting the hit rate."""
    buffer = BranchTargetBuffer(entries)

    for address, target in zip(addresses, targets):
        if buffer.lookup(address) != target:
            buffer.update(address, target)

    return {"hits": buffer.hits, "misses": buffer.misses,
            "hit_rate": buffer.hit_rate()}
