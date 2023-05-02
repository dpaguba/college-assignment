"""Topological sort: an order where every edge points forwards."""

from __future__ import annotations

from collections import deque


def kahn(graph):
    """Repeatedly take a vertex nothing depends on.

    Count how many edges point into each vertex. Anything with a count of zero
    has no unmet prerequisite and can go next; removing it lowers the counts of
    its neighbours, which may free them in turn.

    The cycle test comes free and is the elegant part. If the queue empties
    before every vertex has been output, the remainder all have incoming edges,
    which in a finite graph means they point at each other in a loop. No extra
    machinery is needed to detect it.

    This is what a build system does: `make`, `cargo`, `npm`, the Linux package
    managers and every task runner are running Kahn's algorithm over a
    dependency graph, and "circular dependency detected" is this exact check.
    """
    incoming = {vertex: 0 for vertex in graph.vertices}
    for _, target, _ in graph.edges():
        incoming[target] += 1

    ready = deque(vertex for vertex, count in incoming.items() if count == 0)
    order = []

    while ready:
        vertex = ready.popleft()
        order.append(vertex)
        for neighbour in graph.neighbours(vertex):
            incoming[neighbour] -= 1
            if incoming[neighbour] == 0:
                ready.append(neighbour)

    if len(order) != len(graph):
        remaining = [v for v in graph.vertices if v not in set(order)]
        raise ValueError(f"a cycle involves {remaining}")

    return order


def topological_sort_dfs(graph):
    """The same order, read off a depth-first search backwards.

    A vertex finishes only after everything reachable from it has finished, so
    the reverse of the finishing order is a topological order. That is the
    whole proof, and it is why DFS finishing times keep turning up: they encode
    the dependency structure without anyone counting anything.

    A grey vertex encountered during the search means the path has looped, so
    the cycle test is again free, just found differently.
    """
    WHITE, GREY, BLACK = 0, 1, 2
    colour = {vertex: WHITE for vertex in graph.vertices}
    finished = []

    for root in graph.vertices:
        if colour[root] != WHITE:
            continue
        stack = [(root, iter(graph.neighbours(root)))]
        colour[root] = GREY

        while stack:
            vertex, neighbours = stack[-1]
            advanced = False
            for neighbour in neighbours:
                if colour[neighbour] == GREY:
                    raise ValueError(f"a cycle reaches back to {neighbour}")
                if colour[neighbour] == WHITE:
                    colour[neighbour] = GREY
                    stack.append((neighbour, iter(graph.neighbours(neighbour))))
                    advanced = True
                    break
            if not advanced:
                colour[vertex] = BLACK
                finished.append(vertex)
                stack.pop()

    return list(reversed(finished))
