"""Union-Find: which things are connected, answered in almost constant time."""

from __future__ import annotations

class UnionFind:
    """A collection of disjoint sets, with merge and query as the only operations.

    The question is deliberately narrow: not what a component contains, only
    whether two things are in the same one. Giving up the first buys an answer
    to the second that is faster than any graph traversal.

    Each set is a tree, and the root is the set's name. `find` walks to the
    root; `union` points one root at the other. On its own that degrades into a
    chain, so two refinements keep it flat, and they are the reason this
    structure is famous:

    **Union by rank.** The shorter tree hangs under the taller one, so the
    height only grows when two trees of equal height meet, which needs twice as
    many elements each time.

    **Path compression.** After `find` walks to the root, every node it passed
    is pointed straight at that root, so the next query on any of them is one
    step.

    Together they give O(α(n)) amortised, where α is the inverse Ackermann
    function. It is below 5 for any n that could be stored in this universe, so
    the operations are constant in every practical sense while not being
    constant in theory. That gap is the whole reason the analysis is famous.

    This is the engine inside Kruskal's algorithm, and inside every "are these
    two accounts the same person" deduplication job.
    """

    def __init__(self, items=()):
        """One singleton class per item."""
        self._parent: dict = {}
        self._rank: dict = {}
        self.count = 0
        for item in items:
            self.add(item)

    def add(self, item):
        """Put an item in a set of its own, if it is not already known."""
        if item not in self._parent:
            self._parent[item] = item
            self._rank[item] = 0
            self.count += 1

    def find(self, item):
        """The name of the set containing `item`, flattening the path on the way."""
        if item not in self._parent:
            raise KeyError(f"{item!r} is not in any set")

        root = item
        while self._parent[root] != root:
            root = self._parent[root]

        while self._parent[item] != root:
            self._parent[item], item = root, self._parent[item]

        return root

    def union(self, left, right):
        """Merge two sets. Returns False when they were already one."""
        left_root, right_root = self.find(left), self.find(right)
        if left_root == right_root:
            return False

        if self._rank[left_root] < self._rank[right_root]:
            left_root, right_root = right_root, left_root
        self._parent[right_root] = left_root
        if self._rank[left_root] == self._rank[right_root]:
            self._rank[left_root] += 1

        self.count -= 1
        return True

    def connected(self, left, right):
        """True when both items are in the same set, which is two find calls."""
        return self.find(left) == self.find(right)

    def groups(self):
        """The sets themselves, for when the answer really is needed."""
        found: dict = {}
        for item in self._parent:
            found.setdefault(self.find(item), []).append(item)
        return list(found.values())

    def depth_of(self, item):
        """How many hops to the root. Only useful for showing compression works."""
        depth = 0
        while self._parent[item] != item:
            item = self._parent[item]
            depth += 1
        return depth

    def __len__(self):
        """How many entries the structure holds."""
        return len(self._parent)
