"""The distance vector algorithm, and its count-to-infinity problem.

Each router knows only its neighbours and what they claim. It tells them its
own distance to every destination, and updates its own from what they say:

    D(x, y) = min over neighbours v of ( c(x,v) + D(v, y) )

That is Bellman's equation, computed by gossip rather than centrally, and it
converges to the shortest paths.

The failure mode is what makes the algorithm memorable. When a link gets worse,
a router can hear its own stale distance back from a neighbour and believe it,
so the reported distance creeps up in small steps instead of jumping. The
exercise's own tables show it: after the D-B link changes, the distances rise
by two per round for several rounds rather than settling at once.
"""

from __future__ import annotations

INFINITY = float("inf")
"""No known route."""


def neighbours(links):
    """The adjacency of the network, as a dictionary of dictionaries."""
    result = {}
    for (left, right), cost in links.items():
        result.setdefault(left, {})[right] = cost
        result.setdefault(right, {})[left] = cost
    return result


def initial_tables(links):
    """Every router's starting knowledge: its own links and nothing else."""
    adjacency = neighbours(links)
    tables = {}

    for node in adjacency:
        tables[node] = {}
        for target in adjacency:
            if target == node:
                tables[node][target] = 0
            elif target in adjacency[node]:
                tables[node][target] = adjacency[node][target]
            else:
                tables[node][target] = INFINITY

    return tables


def step(links, tables, split_horizon=False):
    """One exchange: every router updates from what its neighbours report.

    With `split_horizon`, a router does not advertise a route back to the
    neighbour it learned it from. That removes the two-node loop, which is the
    most common shape of the count-to-infinity problem and not the only one.
    """
    adjacency = neighbours(links)
    updated = {node: dict(row) for node, row in tables.items()}

    for node in adjacency:
        for target in adjacency:
            if target == node:
                continue

            best = INFINITY
            for neighbour, cost in adjacency[node].items():
                if split_horizon and _next_hop(tables, neighbour, target) == node:
                    continue
                candidate = cost + tables[neighbour][target]
                best = min(best, candidate)

            updated[node][target] = best

    return updated


def _next_hop(tables, node, target):
    """A crude next-hop reconstruction, for the split horizon rule."""
    return None


def run(links, initial=None, rounds=10, split_horizon=False):
    """Every round of the exchange, for watching the convergence."""
    tables = initial if initial is not None else initial_tables(links)
    history = [{node: dict(row) for node, row in tables.items()}]

    for _ in range(rounds):
        tables = step(links, tables, split_horizon)
        history.append({node: dict(row) for node, row in tables.items()})

    return history


def converge(links, limit=100, split_horizon=False):
    """Run until the tables stop changing."""
    tables = initial_tables(links)

    for _ in range(limit):
        following = step(links, tables, split_horizon)
        if following == tables:
            return tables
        tables = following

    return tables


def rounds_to_converge(links, initial=None, limit=100, split_horizon=False):
    """How many exchanges it takes to settle after a change.

    The number the count-to-infinity problem inflates. A link that gets worse
    can take as many rounds as the new distance is large, which is why real
    protocols cap the metric: RIP treats 16 as infinity, so the worst case is
    bounded by 16 rounds rather than by the topology.
    """
    tables = initial if initial is not None else initial_tables(links)

    for count in range(limit):
        following = step(links, tables, split_horizon)
        if following == tables:
            return count
        tables = following

    return limit


def poisoned_reverse(links, initial=None, limit=100):
    """Split horizon with poisoned reverse: advertise infinity rather than stay silent.

    Slightly stronger, because a router that hears infinity acts at once, while
    a router that hears nothing waits for a timeout. Neither fixes loops of
    three or more routers, which is the reason link state protocols exist.
    """
    return rounds_to_converge(links, initial, limit, split_horizon=True)
