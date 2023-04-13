"""Bellman-Ford: relax every edge, V-1 times, and the answers settle."""

from __future__ import annotations

class NegativeCycle(Exception):
    """Raised when costs can be lowered for ever by going round a loop."""

def bellman_ford(graph, start):
    """Return the cheapest cost to every reachable vertex, and the round count.

    Dijkstra commits to a vertex as soon as it comes off the queue, which is
    only sound when edges cannot lower a cost later. Bellman-Ford commits to
    nothing: it relaxes every edge, over and over, until no cost improves.

    The bound is V-1 rounds, and the reason is simple. A shortest path in a
    graph without negative cycles visits at most V vertices, so it has at most
    V-1 edges, and one round extends every known path by one more edge. After
    V-1 rounds every shortest path has had room to form.

    That gives the negative cycle test for free. If a V-th round still improves
    something, some path is using more than V-1 edges, which can only pay off
    by going round a loop that reduces cost, and then no shortest path exists
    at all. That test is the reason the algorithm survives despite being far
    slower than Dijkstra: currency arbitrage and routing loop detection are
    both this check, not the distances.
    """
    if start not in graph:
        raise KeyError(f"{start!r} is not a vertex of this graph")

    costs = {start: 0}
    parents = {start: None}
    edges = list(graph.edges())
    if not graph.directed:
        edges = edges + [(target, source, weight) for source, target, weight in edges]

    rounds = 0
    for _ in range(len(graph) - 1):
        rounds += 1
        changed = False
        for source, target, weight in edges:
            if source in costs and costs[source] + weight < costs.get(target, float("inf")):
                costs[target] = costs[source] + weight
                parents[target] = source
                changed = True
        if not changed:
            break

    for source, target, weight in edges:
        if source in costs and costs[source] + weight < costs.get(target, float("inf")):
            raise NegativeCycle(
                f"the edge {source} -> {target} still improves after {len(graph) - 1} rounds"
            )

    return costs, rounds

def _relax(graph, start):
    """The same sweep, returning the parents rather than the round count."""
    costs = {start: 0}
    parents = {start: None}
    edges = list(graph.edges())
    if not graph.directed:
        edges = edges + [(target, source, weight) for source, target, weight in edges]

    for _ in range(len(graph) - 1):
        changed = False
        for source, target, weight in edges:
            if source in costs and costs[source] + weight < costs.get(target, float("inf")):
                costs[target] = costs[source] + weight
                parents[target] = source
                changed = True
        if not changed:
            break
    return costs, parents

def shortest_path(graph, start, goal):
    """The cheapest path, or None when the goal cannot be reached."""
    costs, _ = bellman_ford(graph, start)
    if goal not in costs:
        return None

    _, parents = _relax(graph, start)
    path = [goal]
    while parents[path[-1]] is not None:
        path.append(parents[path[-1]])
    return list(reversed(path))
