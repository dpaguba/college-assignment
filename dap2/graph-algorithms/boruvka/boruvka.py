"""Borůvka: every component picks its cheapest edge, all at the same time."""

from __future__ import annotations
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "union-find"))

from union_find import UnionFind

def boruvka(graph, count_rounds=False):
    """Return the edges of a minimum spanning tree and their total weight.

    The oldest of the three, from 1926, written to plan an electrical network
    in Moravia, and the one that fits modern hardware best.

    Kruskal and Prim both make one decision at a time: the next cheapest edge,
    the next vertex to absorb. Borůvka has every component choose its own
    cheapest outgoing edge simultaneously, then merges all of them at once.

    Because every component merges with at least one other, the number of
    components at least halves each round, so O(log V) rounds suffice. Each
    round scans the edges once, giving O(E log V).

    The rounds are what make it interesting today: the choices within a round
    are independent, so it parallelises where the other two do not. Modern
    parallel and GPU spanning tree algorithms are Borůvka.

    One detail is load bearing: ties must be broken consistently, otherwise two
    components can each pick a different edge of the same weight between them
    and the result contains a cycle. Comparing on (weight, source, target)
    settles it.

    Ties between edges of equal weight are broken consistently. Without that,
    two components can choose different edges between the same pair and close a
    cycle.
    """
    sets = UnionFind(graph.vertices)
    edges = list(graph.edges())
    chosen = []
    total = 0
    rounds = 0

    while sets.count > 1:
        cheapest: dict = {}
        for source, target, weight in edges:
            left, right = sets.find(source), sets.find(target)
            if left == right:
                continue
            candidate = (weight, source, target)
            for component in (left, right):
                if component not in cheapest or candidate < cheapest[component]:
                    cheapest[component] = candidate

        if not cheapest:
            break

        rounds += 1
        for weight, source, target in cheapest.values():
            if sets.union(source, target):
                chosen.append((source, target, weight))
                total += weight

    return (chosen, total, rounds) if count_rounds else (chosen, total)
