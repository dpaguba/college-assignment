"""The reachability graph: which markings occur and how they are reached.

Everything a bounded net can do is in this graph, so questions that sound
temporal (can it deadlock, can it always finish, how many tokens accumulate)
become questions about a finite object. The cost is the size of the graph,
which is why the invariants in the properties module matter: they answer some
of the same questions without building it.
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "net-structure"))
import net_structure as nets


def reachable(net, limit=20000):
    """Every reachable marking, as a set of hashable markings."""
    return set(graph(net, limit)["nodes"])


def graph(net, limit=20000):
    """The reachability graph, with edges labelled by the transition fired."""
    start = net.key()
    nodes, edges = {start}, []
    frontier = [net]
    while frontier:
        if len(nodes) > limit:
            raise ValueError("граф досяжності перевищив межу")
        current = frontier.pop()
        for transition in current.enabled_transitions():
            following = current.fire(transition)
            edges.append((current.key(), transition, following.key()))
            if following.key() not in nodes:
                nodes.add(following.key())
                frontier.append(following)
    return {"nodes": nodes, "edges": edges, "start": start}


def firing_sequence(net, target, limit=20000):
    """The shortest firing sequence that reaches a target marking."""
    goal = frozenset((place, count) for place, count in target.items() if count)
    if net.key() == goal:
        return []
    seen = {net.key()}
    frontier = [(net, [])]
    while frontier:
        following = []
        for current, path in frontier:
            for transition in current.enabled_transitions():
                after = current.fire(transition)
                if after.key() == goal:
                    return path + [transition]
                if after.key() not in seen:
                    seen.add(after.key())
                    following.append((after, path + [transition]))
                    if len(seen) > limit:
                        return None
        frontier = following
    return None


def marking_of(key):
    """Turn a graph node back into a marking dictionary."""
    return dict(key)
