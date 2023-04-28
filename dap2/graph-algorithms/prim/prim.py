"""Prim: grow one tree, always taking its cheapest edge to the outside."""

from __future__ import annotations

import heapq

def prim(graph, start=None):
    """Return the edges of a minimum spanning tree and their total weight.

    Kruskal considers all edges everywhere and keeps a forest that only becomes
    a tree at the end. Prim keeps one tree from the first step and asks a
    narrower question each time: which single edge leaving the tree is
    cheapest.

    Both rest on the same cut property, applied to different cuts. Kruskal
    takes the cheapest edge across whatever split the edge happens to repair;
    Prim takes the cheapest edge across the split between the tree and
    everything else. Same guarantee, different bookkeeping.

    With a priority queue over the frontier the cost is O(E + V log V), which
    beats Kruskal's O(E log E) on a dense graph, because Kruskal has to sort
    every edge whether or not it is ever used.

    Prim needs a starting vertex and only ever reaches its component, where
    Kruskal produces a forest over the whole graph without being asked.

    An entry that surfaces for a vertex already in the tree is stale: the far
    end joined through a cheaper edge, and the entry is skipped rather than
    removed, since a binary heap cannot delete from the middle.
    """
    if start is None:
        if not graph.vertices:
            return [], 0
        start = graph.vertices[0]
    if start not in graph:
        raise KeyError(f"{start!r} is not a vertex of this graph")

    inside = {start}
    chosen = []
    total = 0
    frontier = [
        (graph.weight(start, neighbour), start, neighbour)
        for neighbour in graph.neighbours(start)
    ]
    heapq.heapify(frontier)

    while frontier:
        weight, source, target = heapq.heappop(frontier)
        if target in inside:
            continue

        inside.add(target)
        chosen.append((source, target, weight))
        total += weight

        for neighbour in graph.neighbours(target):
            if neighbour not in inside:
                heapq.heappush(frontier, (graph.weight(target, neighbour), target, neighbour))

    return chosen, total
