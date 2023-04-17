"""Breadth-first search: visit everything one step away, then two, then three."""

from __future__ import annotations

from collections import deque


def breadth_first_search(graph, start):
    """Return the reachable vertices in order of distance from `start`.

    A queue is the whole algorithm. Because vertices come out in the order they
    went in, everything at distance one is processed before anything at
    distance two, and the wave spreads outward evenly.

    That single property is why BFS finds shortest paths in an unweighted
    graph, and why it stops being correct the moment edges have different
    weights: the wave measures edges crossed, not distance travelled. Dijkstra
    is BFS with the queue replaced by a priority queue, which is precisely the
    fix.

    Marking a vertex when it is queued rather than when it is dequeued matters.
    Marking on dequeue lets a vertex enter the queue several times through
    different neighbours, and on a dense graph that is the difference between
    linear and quadratic.
    """
    if start not in graph:
        raise KeyError(f"{start!r} is not a vertex of this graph")

    seen = {start}
    order = [start]
    queue = deque([start])

    while queue:
        vertex = queue.popleft()
        for neighbour in graph.neighbours(vertex):
            if neighbour not in seen:
                seen.add(neighbour)
                order.append(neighbour)
                queue.append(neighbour)

    return order


def shortest_path(graph, start, goal):
    """The path with the fewest edges, or None when there is none.

    The parent map is built during the same sweep: each vertex remembers who
    reached it first, and first means closest, so following the parents back
    from the goal gives a shortest path without any extra work.
    """
    if start not in graph:
        raise KeyError(f"{start!r} is not a vertex of this graph")
    if start == goal:
        return [start]

    parents = {start: None}
    queue = deque([start])

    while queue:
        vertex = queue.popleft()
        for neighbour in graph.neighbours(vertex):
            if neighbour in parents:
                continue
            parents[neighbour] = vertex
            if neighbour == goal:
                path = [goal]
                while parents[path[-1]] is not None:
                    path.append(parents[path[-1]])
                return list(reversed(path))
            queue.append(neighbour)

    return None


def distances(graph, start):
    """How many edges away every reachable vertex is."""
    measured = {start: 0}
    queue = deque([start])
    while queue:
        vertex = queue.popleft()
        for neighbour in graph.neighbours(vertex):
            if neighbour not in measured:
                measured[neighbour] = measured[vertex] + 1
                queue.append(neighbour)
    return measured
