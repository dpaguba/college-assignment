"""Link state routing: every router learns the whole topology.

Each router floods a description of its own links to everyone, so every router
ends up with the same map and runs Dijkstra's algorithm on it locally. That is
the opposite trade from the distance vector approach: more information per
router and much less time to converge, because nobody is relying on anybody
else's arithmetic.

There is no count to infinity, because no router believes a distance it did not
compute itself.
"""

from __future__ import annotations

import heapq

INFINITY = float("inf")
"""No known route."""


def neighbours(links):
    """The adjacency of the network."""
    result = {}
    for (left, right), cost in links.items():
        result.setdefault(left, {})[right] = cost
        result.setdefault(right, {})[left] = cost
    return result


def dijkstra(links, source):
    """Shortest distances and predecessors from one router.

    The greedy argument works because the costs are non-negative: the nearest
    unvisited node cannot be reached more cheaply through a node that is
    further away. A negative link cost would break that, which is why routing
    metrics are always positive.
    """
    adjacency = neighbours(links)
    distance = {node: INFINITY for node in adjacency}
    previous = {node: None for node in adjacency}
    distance[source] = 0

    queue = [(0, source)]
    settled = set()

    while queue:
        current, node = heapq.heappop(queue)
        if node in settled:
            continue
        settled.add(node)

        for target, cost in adjacency[node].items():
            candidate = current + cost
            if candidate < distance[target]:
                distance[target] = candidate
                previous[target] = node
                heapq.heappush(queue, (candidate, target))

    return {"distance": distance, "previous": previous, "source": source}


def path(result, target):
    """The shortest path to a destination, from a Dijkstra result."""
    route = []
    node = target

    while node is not None:
        route.append(node)
        node = result["previous"][node]

    return list(reversed(route))


def forwarding_table(links, source):
    """The first hop towards every destination.

    A router stores only this, not the whole path: the next router repeats the
    decision. That is what makes forwarding a per-packet table lookup and
    routing a periodic computation, and it is why the two words are not
    synonyms.
    """
    result = dijkstra(links, source)
    table = {}

    for target in result["distance"]:
        if target == source:
            continue
        route = path(result, target)
        if len(route) > 1:
            table[target] = route[1]

    return table


def messages_per_change(nodes, links, kind):
    """How much traffic one topology change causes.

    Link state floods to every link in both directions, so the cost is
    proportional to the links and independent of how bad the news is. Distance
    vector sends only to neighbours, so one change is cheaper and a change that
    triggers count to infinity is not.
    """
    if kind == "link state":
        return links * 2
    return nodes * (nodes - 1)


def converged_tables(links):
    """Every router's forwarding table, computed independently.

    They agree because they are computed from the same map, which is the whole
    argument for the approach: consistency comes from shared information rather
    than from a protocol that has to establish it.
    """
    return {node: forwarding_table(links, node) for node in neighbours(links)}
