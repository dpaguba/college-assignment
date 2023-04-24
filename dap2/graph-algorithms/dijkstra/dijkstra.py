"""Dijkstra: breadth-first search with a priority queue instead of a queue."""

from __future__ import annotations

import heapq


def dijkstra(graph, start):
    """Return the cheapest cost to every reachable vertex, and the parents.

    BFS spreads by edge count, so it is right only when every edge costs the
    same. Replace the queue with a priority queue keyed by distance and the
    wave spreads by cost instead. That substitution is the entire algorithm.

    Correctness rests on one assumption: when a vertex comes off the queue, no
    cheaper route to it can still appear. That holds because every edge adds a
    non-negative amount, so any unfinished route is already at least as
    expensive. **A single negative edge breaks the argument**, and Dijkstra
    then returns a wrong answer confidently, which is why this raises rather
    than guessing. Bellman-Ford is the algorithm for that case.

    Rather than decreasing a key in the heap, which Python's heapq cannot do,
    an improved distance is pushed as a second entry and the stale one is
    skipped when it surfaces. That is the standard lazy variant.
    """
    if start not in graph:
        raise KeyError(f"{start!r} is not a vertex of this graph")
    for _, _, weight in graph.edges():
        if weight < 0:
            raise ValueError(
                "Dijkstra cannot handle negative weights; use Bellman-Ford"
            )

    costs = {start: 0}
    parents = {start: None}
    finished = set()
    queue = [(0, start)]

    while queue:
        cost, vertex = heapq.heappop(queue)
        if vertex in finished:
            continue
        finished.add(vertex)

        for neighbour in graph.neighbours(vertex):
            candidate = cost + graph.weight(vertex, neighbour)
            if candidate < costs.get(neighbour, float("inf")):
                costs[neighbour] = candidate
                parents[neighbour] = vertex
                heapq.heappush(queue, (candidate, neighbour))

    return costs, parents


def shortest_path(graph, start, goal):
    """The cheapest path, or None when the goal cannot be reached."""
    costs, parents = dijkstra(graph, start)
    if goal not in costs:
        return None
    path = [goal]
    while parents[path[-1]] is not None:
        path.append(parents[path[-1]])
    return list(reversed(path))
