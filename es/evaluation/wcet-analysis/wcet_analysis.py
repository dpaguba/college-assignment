"""Worst case execution time: the longest path, and why measuring is not enough.

The analysis walks the control flow graph and takes the most expensive path,
which needs a bound on every loop, because without one the longest path is
unbounded and the question has no answer. That is why loop bounds are the
first thing a WCET tool asks for.

Measuring gives a number that is always a lower bound of the truth: the
worst case input may not have been among the ones tried. Analysis gives an
upper bound that is safe and pessimistic. The gap between them is the price
of soundness, and it is what the module reports.
"""


def longest_path(blocks, edges, start, end, bounds=None):
    """The cost of the most expensive path through the graph.

    Raises when a cycle has no bound, since the answer would be unbounded.
    A bound turns the cycle into a fixed number of repetitions, which is the
    information a tool cannot infer and a programmer has to supply.
    """
    bounds = bounds or {}
    successors = {}
    for source, target in edges:
        successors.setdefault(source, []).append(target)
    best = {}

    def walk(node, seen):
        """The most expensive path from a node to the end."""
        if node == end:
            return blocks[node]
        if node in seen:
            if node in bounds:
                return 0
            raise ValueError("unbounded loop at %s" % node)
        targets = successors.get(node, [])
        if not targets:
            raise ValueError("no path from %s to %s" % (node, end))
        repetitions = bounds.get(node, 1) if node in targets else 1
        if node in targets and node not in bounds:
            raise ValueError("unbounded loop at %s" % node)
        onward = [walk(target, seen | {node})
                  for target in targets if target != node]
        if not onward:
            raise ValueError("no path from %s to %s" % (node, end))
        return blocks[node] * repetitions + max(onward)

    return walk(start, frozenset())


def measurement_versus_analysis():
    """A measured maximum against an analysed bound on the same program.

    The measured value comes from a set of inputs and the analysed one from
    the longest path, so the second is larger by construction. A tool that
    reported the first as the worst case would be reporting the largest
    number it happened to see.
    """
    blocks = {"a": 1, "t": 10, "f": 2, "e": 1}
    edges = [("a", "t"), ("a", "f"), ("t", "e"), ("f", "e")]
    analysed = longest_path(blocks, edges, "a", "e")
    measured = max(blocks["a"] + blocks["f"] + blocks["e"] for _ in range(20))
    return {"analysed bound": analysed, "measured maximum": measured,
            "overestimation": analysed - measured}


def cache_effect(hits, misses, hit_cost, miss_cost):
    """The cost of a memory access pattern, and why analysis is pessimistic.

    A safe analysis assumes a miss whenever it cannot prove a hit, so the
    bound grows with everything the analysis cannot see, which is why a cache
    makes programs faster and their worst case harder to bound.
    """
    optimistic = (hits + misses) * hit_cost
    realistic = hits * hit_cost + misses * miss_cost
    pessimistic = (hits + misses) * miss_cost
    return {"optimistic": optimistic, "realistic": realistic,
            "safe bound": pessimistic}
