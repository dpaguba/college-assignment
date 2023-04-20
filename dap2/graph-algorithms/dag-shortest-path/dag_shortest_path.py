"""Shortest paths in a DAG: relax the edges in topological order, once each."""

from __future__ import annotations


def topological_order(graph):
    """Vertices such that every edge points forward. Raises on a cycle."""
    incoming = {vertex: 0 for vertex in graph.vertices}
    for _, target, _ in graph.edges():
        incoming[target] += 1

    ready = [vertex for vertex, count in incoming.items() if count == 0]
    order = []
    while ready:
        vertex = ready.pop()
        order.append(vertex)
        for neighbour in graph.neighbours(vertex):
            incoming[neighbour] -= 1
            if incoming[neighbour] == 0:
                ready.append(neighbour)

    if len(order) != len(graph):
        raise ValueError("the graph has a cycle, so no topological order exists")
    return order


def dag_shortest_path(graph, start):
    """Cheapest cost to every vertex, in O(V + E), negative weights allowed.

    Dijkstra costs E + V log V and refuses negative edges. Bellman-Ford accepts
    them and costs V·E. On a graph without cycles, both are unnecessary.

    Sort the vertices topologically and relax each vertex's outgoing edges once,
    in that order. When a vertex is reached, every path into it has already been
    considered, because every such path comes from earlier in the order. One
    pass, linear time, and the sign of the weights never enters the argument,
    which is why negative edges are fine here and nowhere else this cheap.

    The catch is in the name: it needs a DAG. On anything cyclic there is no
    order to relax in, and this refuses rather than returning nonsense.
    """
    if start not in graph:
        raise KeyError(f"{start!r} is not a vertex of this graph")

    costs = {start: 0}
    parents = {start: None}

    for vertex in topological_order(graph):
        if vertex not in costs:
            continue
        for neighbour in graph.neighbours(vertex):
            candidate = costs[vertex] + graph.weight(vertex, neighbour)
            if candidate < costs.get(neighbour, float("inf")):
                costs[neighbour] = candidate
                parents[neighbour] = vertex

    return costs, parents


def dag_longest_path(graph, start):
    """The most expensive path, which is NP-hard in general and linear here.

    Longest path is one of the classic NP-hard problems, because a cycle can be
    walked repeatedly. Take the cycles away and it collapses into the same
    single pass, with the comparison turned around. That gap between the general
    problem and the acyclic one is the point worth remembering: this is the
    algorithm behind every project schedule's critical path.
    """
    if start not in graph:
        raise KeyError(f"{start!r} is not a vertex of this graph")

    costs = {start: 0}
    parents = {start: None}

    for vertex in topological_order(graph):
        if vertex not in costs:
            continue
        for neighbour in graph.neighbours(vertex):
            candidate = costs[vertex] + graph.weight(vertex, neighbour)
            if candidate > costs.get(neighbour, float("-inf")):
                costs[neighbour] = candidate
                parents[neighbour] = vertex

    return costs, parents
