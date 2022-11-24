"""How fast the iteration settles, and what decides the rate.

The power iteration converges geometrically with a rate given by the damping
factor: the error is multiplied by roughly that factor at every step. A
smaller damping factor therefore converges faster and describes a surfer who
follows links less often, so the usual value of 0.85 is a compromise between
the model and the computation.
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "pagerank"))
import pagerank


def iterations(edges, damping=0.85, tolerance=1e-8, limit=1000):
    """How many steps the iteration needs to settle."""
    nodes = sorted({node for edge in edges for node in edge})
    count = len(nodes)
    ranks = {node: 1 / count for node in nodes}
    for step in range(1, limit + 1):
        following = _step(edges, ranks, damping)
        difference = max(abs(following[node] - ranks[node]) for node in nodes)
        ranks = following
        if difference < tolerance:
            return {"steps": step, "ranks": ranks}
    return {"steps": limit, "ranks": ranks}


def _step(edges, ranks, damping):
    """One iteration of the power method."""
    nodes = sorted({node for edge in edges for node in edge})
    outgoing = {node: [] for node in nodes}
    for source, target in edges:
        outgoing[source].append(target)
    count = len(nodes)
    following = {node: (1 - damping) / count for node in nodes}
    leaked = 0.0
    for node in nodes:
        targets = outgoing[node]
        if not targets:
            leaked += damping * ranks[node]
            continue
        share = damping * ranks[node] / len(targets)
        for target in targets:
            following[target] += share
    for node in nodes:
        following[node] += leaked / count
    return following


def error_trace(edges, steps, damping=0.85):
    """The distance from the final ranks after each step."""
    target = pagerank.compute(edges, damping)
    nodes = sorted(target)
    ranks = {node: 1 / len(nodes) for node in nodes}
    errors = []
    for _ in range(steps):
        ranks = _step(edges, ranks, damping)
        errors.append(max(abs(ranks[node] - target[node]) for node in nodes))
    return errors
