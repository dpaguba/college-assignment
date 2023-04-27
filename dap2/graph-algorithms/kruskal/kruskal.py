"""Kruskal: sort the edges, take any that does not close a cycle."""

from __future__ import annotations
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "union-find"))

from union_find import UnionFind


def kruskal(graph):
    """Return the edges of a minimum spanning tree and their total weight.

    The algorithm is two lines of English: sort the edges by weight, and take
    each one unless it would close a cycle.

    Why that is optimal is the cut property. For any way of splitting the
    vertices into two groups, the cheapest edge crossing the split belongs to
    some minimum spanning tree. Taking edges in increasing order means every
    edge taken is the cheapest across the split it repairs, so nothing better
    was passed over.

    The interesting part is "would close a cycle". Checking by traversal costs
    O(V) per edge and the whole thing becomes O(E·V). Union-Find answers the
    same question in almost constant time, so the sort dominates and the total
    is O(E log E). This is the algorithm that made Union-Find worth inventing.

    On a disconnected graph it produces a spanning forest rather than failing,
    which falls out of the method without a special case.
    """
    sets = UnionFind(graph.vertices)
    chosen = []
    total = 0

    for source, target, weight in sorted(graph.edges(), key=lambda edge: edge[2]):
        if sets.union(source, target):
            chosen.append((source, target, weight))
            total += weight

    return chosen, total
