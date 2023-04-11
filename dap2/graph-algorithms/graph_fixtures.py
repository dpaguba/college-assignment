"""Graphs the tests share, each chosen to break something specific."""

from __future__ import annotations

from graph import Graph


def line():
    """a - b - c - d, the simplest thing that has a path."""
    g = Graph()
    for left, right in (("a", "b"), ("b", "c"), ("c", "d")):
        g.add_edge(left, right)
    return g


def diamond():
    """Two routes of different length between the same pair."""
    g = Graph(directed=True)
    g.add_edge("s", "a", 1)
    g.add_edge("s", "b", 4)
    g.add_edge("a", "b", 2)
    g.add_edge("b", "t", 1)
    g.add_edge("a", "t", 6)
    return g


def disconnected():
    """Two components, so anything assuming reachability breaks."""
    g = Graph()
    g.add_edge("a", "b")
    g.add_edge("c", "d")
    g.add_vertex("lonely")
    return g


def weighted():
    """The standard textbook graph for shortest paths and spanning trees."""
    g = Graph()
    for left, right, cost in (
        ("a", "b", 4), ("a", "c", 8), ("b", "c", 11), ("b", "d", 8),
        ("c", "e", 7), ("d", "e", 2), ("d", "f", 7), ("e", "f", 6),
    ):
        g.add_edge(left, right, cost)
    return g


def negative_edges():
    """Negative weights but no negative cycle: Dijkstra's blind spot."""
    g = Graph(directed=True)
    g.add_edge("s", "a", 4)
    g.add_edge("s", "b", 5)
    g.add_edge("a", "c", 3)
    g.add_edge("b", "a", -3)
    g.add_edge("c", "t", 2)
    return g


def negative_cycle():
    """A loop that gets cheaper every time round, so no shortest path exists."""
    g = Graph(directed=True)
    g.add_edge("s", "a", 1)
    g.add_edge("a", "b", 2)
    g.add_edge("b", "c", -6)
    g.add_edge("c", "a", 2)
    return g


def dag():
    """Dependencies: shoes cannot go on before socks."""
    g = Graph(directed=True)
    for before, after in (
        ("socks", "shoes"), ("underwear", "trousers"), ("trousers", "shoes"),
        ("trousers", "belt"), ("shirt", "belt"), ("shirt", "tie"), ("tie", "jacket"),
        ("belt", "jacket"),
    ):
        g.add_edge(before, after)
    return g


def cyclic():
    """A directed cycle, so topological order cannot exist."""
    g = Graph(directed=True)
    g.add_edge("a", "b")
    g.add_edge("b", "c")
    g.add_edge("c", "a")
    return g


def strongly_connected():
    """Four strongly connected components, the standard Kosaraju example."""
    g = Graph(directed=True)
    for source, target in (
        ("a", "b"), ("b", "c"), ("c", "a"), ("b", "d"), ("d", "e"),
        ("e", "f"), ("f", "d"), ("g", "f"), ("g", "h"), ("h", "g"),
    ):
        g.add_edge(source, target)
    return g


def with_bridges():
    """Two triangles joined by one edge, which is the only bridge."""
    g = Graph()
    for left, right in (
        ("a", "b"), ("b", "c"), ("c", "a"), ("c", "d"),
        ("d", "e"), ("e", "f"), ("f", "d"),
    ):
        g.add_edge(left, right)
    return g


def grid(width=6, height=5, blocked=()):
    """A lattice with optional walls, for A* and BFS on something spatial."""
    g = Graph()
    for x in range(width):
        for y in range(height):
            if (x, y) in blocked:
                continue
            g.add_vertex((x, y))
            for dx, dy in ((1, 0), (0, 1)):
                other = (x + dx, y + dy)
                if other[0] < width and other[1] < height and other not in blocked:
                    g.add_edge((x, y), other, 1)
    return g
