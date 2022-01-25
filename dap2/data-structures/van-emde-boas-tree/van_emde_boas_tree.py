"""van Emde Boas tree: O(log log u) by recursing on the universe, not the data."""

from __future__ import annotations

class VanEmdeBoasTree:
    """A set of small integers where every operation costs O(log log u).

    Every balanced tree here recurses on the number of elements: n keys, log n
    levels. This one recurses on the size of the universe instead. A universe
    of u values splits into √u clusters of √u values each, and a query descends
    into one cluster, so the universe is square-rooted at every step. Halving
    the exponent log u repeatedly gives log log u.

    The numbers are worth stating. Over 32-bit keys, a balanced tree needs
    about 32 comparisons; this needs 5. Successor and predecessor are the same
    cost, which no hash table can do at all.

    The price is space: O(u), not O(n). A tree over 32-bit keys allocates for
    four billion slots whether it holds ten values or a billion, which is why
    the structure is famous and rare. Y-fast tries reach the same time bound in
    O(n) space and are what gets used in practice.

    Two details carry the bound. The minimum is stored in the summary and never
    inserted into a cluster, so an insert into an empty cluster stops
    immediately, and each level makes only one recursive call rather than two.

    The universe is rounded up to a power of two so that halving the bits is
    exact at every level.
    """

    def __init__(self, universe):
        """A tree over a universe rounded up to a power of two."""
        if universe < 2:
            universe = 2
        size = 2
        while size < universe:
            size *= 2
        self._universe = size
        self._min = None
        self._max = None
        self._bits = size.bit_length() - 1

        if size > 2:
            self._lower_bits = self._bits // 2
            self._cluster_size = 1 << self._lower_bits
            cluster_count = size // self._cluster_size
            self._summary = VanEmdeBoasTree(cluster_count)
            self._clusters = [
                VanEmdeBoasTree(self._cluster_size) for _ in range(cluster_count)
            ]
        else:
            self._summary = None
            self._clusters = []

    def _high(self, key):
        """The cluster a key belongs to."""
        return key >> self._lower_bits

    def _low(self, key):
        """The position of a key inside its cluster."""
        return key & (self._cluster_size - 1)

    def _index(self, high, low):
        """The key that a cluster and a position stand for."""
        return (high << self._lower_bits) | low

    def minimum(self):
        """Smallest key, or None.

        O(1), because the minimum is stored outside the clusters.
        """
        return self._min

    def maximum(self):
        """Largest key, or None. O(1), for the same reason."""
        return self._max

    def insert(self, key):
        """Add a key in O(log log u).

        When the new key is smaller than the stored minimum, the old minimum
        moves down into a cluster and the new key takes its place, which is
        what limits the recursion to one call per level.
        """
        if not 0 <= key < self._universe:
            raise ValueError(f"key {key} is outside the universe of {self._universe}")
        if self._min is None:
            self._min = self._max = key
            return
        if key == self._min or key == self._max:
            return

        if key < self._min:
            key, self._min = self._min, key

        if self._universe > 2:
            high, low = self._high(key), self._low(key)
            if self._clusters[high].minimum() is None:
                self._summary.insert(high)
                self._clusters[high]._insert_into_empty(low)
            else:
                self._clusters[high].insert(low)

        if key > self._max:
            self._max = key

    def _insert_into_empty(self, key):
        """Stores the first key, which needs no recursion."""
        self._min = self._max = key

    def delete(self, key):
        """Remove a key in O(log log u)."""
        if self._min is None or not 0 <= key < self._universe:
            return False
        if key not in self:
            return False

        if self._min == self._max:
            self._min = self._max = None
            return True

        if self._universe == 2:
            self._min = self._max = 1 if key == 0 else 0
            return True

        if key == self._min:
            first_cluster = self._summary.minimum()
            key = self._index(first_cluster, self._clusters[first_cluster].minimum())
            self._min = key

        high, low = self._high(key), self._low(key)
        self._clusters[high].delete(low)

        if self._clusters[high].minimum() is None:
            self._summary.delete(high)
            if key == self._max:
                summary_max = self._summary.maximum()
                if summary_max is None:
                    self._max = self._min
                else:
                    self._max = self._index(
                        summary_max, self._clusters[summary_max].maximum()
                    )
        elif key == self._max:
            self._max = self._index(high, self._clusters[high].maximum())

        return True

    def successor(self, key):
        """The smallest stored value strictly greater than `key`."""
        if self._universe == 2:
            return 1 if key == 0 and self._max == 1 else None
        if self._min is not None and key < self._min:
            return self._min

        high, low = self._high(key), self._low(key)
        cluster_max = self._clusters[high].maximum()
        if cluster_max is not None and low < cluster_max:
            return self._index(high, self._clusters[high].successor(low))

        next_cluster = self._summary.successor(high)
        if next_cluster is None:
            return None
        return self._index(next_cluster, self._clusters[next_cluster].minimum())

    def predecessor(self, key):
        """The largest stored value strictly smaller than `key`."""
        if self._universe == 2:
            return 0 if key == 1 and self._min == 0 else None
        if self._max is not None and key > self._max:
            return self._max

        high, low = self._high(key), self._low(key)
        cluster_min = self._clusters[high].minimum()
        if cluster_min is not None and low > cluster_min:
            return self._index(high, self._clusters[high].predecessor(low))

        previous_cluster = self._summary.predecessor(high)
        if previous_cluster is None:
            return self._min if self._min is not None and key > self._min else None
        return self._index(
            previous_cluster, self._clusters[previous_cluster].maximum()
        )

    def keys(self):
        """Every key in ascending order, by walking successors from the minimum."""
        key = self._min
        while key is not None:
            yield key
            key = self.successor(key)

    def __contains__(self, key):
        """Whether the key is stored."""
        if not 0 <= key < self._universe or self._min is None:
            return False
        if key == self._min or key == self._max:
            return True
        if self._universe == 2:
            return False
        return self._low(key) in self._clusters[self._high(key)]

    def __len__(self):
        """How many entries the structure holds."""
        return sum(1 for _ in self.keys())
