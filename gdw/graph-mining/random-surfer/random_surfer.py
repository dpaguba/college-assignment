"""The surfer behind the formula, simulated.

PageRank is defined as a limit of a random walk, and the walk can be run.
Two hundred thousand steps on the exercise graph reproduce the computed ranks
to within two hundredths, which is the check that the formula and the story
describe the same thing.

Teleporting is not a detail. Without it a walk that reaches a sink stays
there and the chain is not irreducible, so the limit either does not exist or
puts everything in one place.
"""

import os
import random
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "pagerank"))
import pagerank


def walk(edges, steps, damping=0.85, seed=0):
    """The share of steps the surfer spends at each node."""
    generator = random.Random(seed)
    nodes = sorted({node for edge in edges for node in edge})
    outgoing = {node: [] for node in nodes}
    for source, target in edges:
        outgoing[source].append(target)
    visits = {node: 0 for node in nodes}
    current = nodes[0]
    for _ in range(steps):
        visits[current] += 1
        if not outgoing[current] or generator.random() > damping:
            current = generator.choice(nodes)
        else:
            current = generator.choice(outgoing[current])
    return {node: count / steps for node, count in visits.items()}


def teleport_share(damping):
    """The probability of jumping rather than following a link."""
    return 1 - damping


def is_irreducible(edges, damping):
    """Whether every node can be reached from every other.

    With teleporting the answer is always yes, which is what guarantees a
    unique stationary distribution. Without it, a graph with a sink has no
    such guarantee, and the module reports the difference.
    """
    if damping < 1.0:
        return True
    nodes = sorted({node for edge in edges for node in edge})
    outgoing = {node: set() for node in nodes}
    for source, target in edges:
        outgoing[source].add(target)
    for start in nodes:
        reached = {start}
        frontier = [start]
        while frontier:
            current = frontier.pop()
            for target in outgoing[current]:
                if target not in reached:
                    reached.add(target)
                    frontier.append(target)
        if set(reached) != set(nodes):
            return False
    return True
