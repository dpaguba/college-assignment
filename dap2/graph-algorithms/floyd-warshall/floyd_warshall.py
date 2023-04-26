"""Floyd-Warshall: every shortest path, from three nested loops."""

from __future__ import annotations


class NegativeCycle(Exception):
    """Raised when a vertex can reach itself at negative cost."""


def floyd_warshall(graph):
    """Cost between every pair of vertices, and the midpoints to rebuild paths.

    Running Dijkstra from every vertex costs V·(E + V log V). This costs V³ and
    is usually faster on a dense graph, because there is nothing in it but
    array access: no heap, no queue, no allocation.

    The idea is a beautifully small induction. Let the vertices be numbered, and
    let D(k) hold the cheapest costs using only the first k vertices as
    intermediates. Then D(k) is D(k-1) with one question asked per pair: is it
    cheaper to go through vertex k? The answer needs only D(k-1), so the whole
    thing is one array updated in place, and the outer loop is over the allowed
    intermediates rather than over anything geometric.

    **The order of the loops is the algorithm.** Putting k innermost gives a
    program that runs, produces plausible numbers and is wrong, which is the
    single most common way to get this wrong.

    A negative value on the diagonal afterwards means some vertex reaches itself
    at a negative cost, which is a negative cycle.
    """
    vertices = graph.vertices
    infinity = float("inf")
    costs = {source: {target: infinity for target in vertices} for source in vertices}
    through = {source: {target: None for target in vertices} for source in vertices}

    for vertex in vertices:
        costs[vertex][vertex] = 0
    for source, target, weight in graph.edges():
        costs[source][target] = min(costs[source][target], weight)
        through[source][target] = target
        if not graph.directed:
            costs[target][source] = min(costs[target][source], weight)
            through[target][source] = source

    for middle in vertices:
        for source in vertices:
            if costs[source][middle] == infinity:
                continue
            for target in vertices:
                candidate = costs[source][middle] + costs[middle][target]
                if candidate < costs[source][target]:
                    costs[source][target] = candidate
                    through[source][target] = through[source][middle]

    for vertex in vertices:
        if costs[vertex][vertex] < 0:
            raise NegativeCycle(f"{vertex} reaches itself at cost {costs[vertex][vertex]}")

    return costs, through


def path_between(through, source, target):
    """Rebuild one path from the table of first steps."""
    if through[source][target] is None:
        return None
    path = [source]
    while path[-1] != target:
        path.append(through[path[-1]][target])
    return path


def transitive_closure(graph):
    """Who can reach whom, which is the same loop with booleans.

    Replacing addition with "and" and minimum with "or" turns shortest paths
    into reachability. That substitution is Warshall's original 1962 algorithm,
    and it is the same shape as matrix multiplication over a different semiring,
    which is why the three loops keep reappearing in unrelated places.
    """
    vertices = graph.vertices
    reachable = {
        source: {target: source == target for target in vertices} for source in vertices
    }
    for source, target, _ in graph.edges():
        reachable[source][target] = True
        if not graph.directed:
            reachable[target][source] = True

    for middle in vertices:
        for source in vertices:
            if not reachable[source][middle]:
                continue
            for target in vertices:
                if reachable[middle][target]:
                    reachable[source][target] = True

    return reachable
