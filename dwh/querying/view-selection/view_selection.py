"""Choosing which aggregates to store, under a budget.

The greedy rule takes the view with the largest benefit, where the benefit is
how much it lowers the cost of the queries it can answer given what is
already chosen. It is the standard algorithm and it is not optimal, which the
module shows with a case where a different pair beats it.

The benefit of a view falls once a view above it is chosen, because the
queries it would have helped are already cheap. That diminishing return is
what makes the greedy rule reasonable and what stops it from being exact.
"""

import itertools
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..",
                                "materialized-views"))
import materialized_views


def benefit(sizes, candidate, chosen):
    """How much materialising a view lowers the total query cost."""
    before = total_cost(sizes, chosen)
    after = total_cost(sizes, set(chosen) | {candidate})
    return before - after


def total_cost(sizes, chosen):
    """The cost of answering every query with the chosen views.

    The base cube is always available, so a query never becomes impossible;
    it becomes expensive, and the total is what the selection lowers.
    """
    base = max(sizes, key=lambda view: len(view))
    available = set(chosen) | {base}
    total = 0
    for query in sizes:
        usable = [sizes[view] for view in available
                  if materialized_views.answers(view, query)]
        total += min(usable)
    return total


def greedy(sizes, budget):
    """The views the greedy rule picks, in order."""
    base = max(sizes, key=lambda view: len(view))
    chosen = []
    for _ in range(budget):
        candidates = [view for view in sizes
                      if view not in chosen and view != base]
        if not candidates:
            break
        best = max(candidates, key=lambda view: benefit(sizes, view,
                                                        set(chosen)))
        chosen.append(best)
    return chosen


def greedy_versus_optimal():
    """A case where the greedy choice is beaten by an exhaustive search."""
    sizes = {frozenset({"a", "b", "c"}): 1000, frozenset({"a", "b"}): 900,
             frozenset({"a", "c"}): 500, frozenset({"b", "c"}): 500,
             frozenset({"a"}): 100, frozenset({"b"}): 100,
             frozenset({"c"}): 100, frozenset(): 1}
    base = max(sizes, key=lambda view: len(view))
    greedy_cost = total_cost(sizes, set(greedy(sizes, 2)))
    best = None
    candidates = [view for view in sizes if view != base]
    for pair in itertools.combinations(candidates, 2):
        value = total_cost(sizes, set(pair))
        best = value if best is None else min(best, value)
    return {"greedy": greedy_cost, "optimal": best}
