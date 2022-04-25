"""Held-Karp: the travelling salesman, exactly, in exponential rather than factorial time.

The city limit is where the table stops fitting in memory: it holds 2^n times n
entries.
"""

from __future__ import annotations

from itertools import combinations

MAX_CITIES = 20

def held_karp(distances):
    """Return the cheapest tour visiting every city once, and the tour itself.

    Trying every order costs (n-1)! which is 3.6 million at n=11 and beyond
    reach by n=15. Held and Karp's 1962 algorithm gets it to O(n²·2ⁿ), which is
    still exponential and is an enormous improvement: 2²⁰ is a million where
    19! is 121 quadrillion.

    The state is a **set** rather than an index, which is what makes this
    different from everything else in this folder. `best[S][j]` is the cheapest
    route that starts at city 0, visits exactly the cities in S, and ends at j.
    Extending it means adding one unvisited city to the end, and the same
    subset arrived at by different orders is computed once instead of once per
    order. That collapse from orders to subsets is the whole saving.

    It remains the fastest known exact algorithm for the general travelling
    salesman problem. Sixty years of work has not improved the exponent, which
    is itself worth knowing: the problem is NP-hard, and this is what "we can
    do better than brute force but not much" looks like in practice.

    Above twenty cities the table needs more memory than it is reasonable to
    ask for, so this refuses rather than thrashing.
    """
    count = len(distances)
    if count > MAX_CITIES:
        raise ValueError(
            f"{count} cities needs a table of 2^{count} entries; the limit here is {MAX_CITIES}"
        )
    if count <= 1:
        return 0, [0, 0]

    best: dict = {}
    parent: dict = {}

    for city in range(1, count):
        best[(1 << city, city)] = distances[0][city]
        parent[(1 << city, city)] = 0

    for size in range(2, count):
        for group in combinations(range(1, count), size):
            subset = 0
            for city in group:
                subset |= 1 << city
            for last in group:
                without = subset & ~(1 << last)
                candidates = [
                    (best[(without, previous)] + distances[previous][last], previous)
                    for previous in group
                    if previous != last and (without, previous) in best
                ]
                if candidates:
                    best[(subset, last)], parent[(subset, last)] = min(candidates)

    everything = (1 << count) - 2  # every city except the start
    cost, last = min(
        (best[(everything, city)] + distances[city][0], city) for city in range(1, count)
    )

    tour = [0]
    subset = everything
    while last != 0:
        tour.append(last)
        previous = parent[(subset, last)]
        subset &= ~(1 << last)
        last = previous
    tour.append(0)
    return cost, list(reversed(tour))
