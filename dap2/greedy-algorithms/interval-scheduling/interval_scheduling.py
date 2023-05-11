"""Interval scheduling: fit the most non-overlapping intervals into a resource."""

from __future__ import annotations

def select(intervals):
    """Return the largest set of intervals that do not overlap.

    The rule is one line: **take the interval that finishes earliest**, discard
    everything it overlaps, repeat.

    Why that is optimal is an exchange argument, and it is the cleanest one in
    the course. Take any optimal solution. Its first interval finishes no
    earlier than the greedy choice, by definition of "earliest finishing".
    Swapping it for the greedy choice cannot conflict with anything later, so
    the result is still valid and still the same size. Repeating the swap turns
    any optimal solution into the greedy one without ever losing an interval,
    so the greedy one is optimal too.

    That argument is what separates a greedy algorithm that works from one that
    merely looks reasonable, and the two functions below exist to show the
    difference.
    """
    if not intervals:
        return []

    chosen = []
    finished = float("-inf")
    for start, end in sorted(intervals, key=lambda interval: interval[1]):
        if start >= finished:
            chosen.append((start, end))
            finished = end
    return chosen

by_earliest_finish = select

def by_earliest_start(intervals):
    """Take whatever starts first. Plausible, and wrong.

    One long interval starting at zero swallows the whole day and blocks
    everything after it. On [(0,10), (1,2), (3,4)] this returns one interval
    where two fit.
    """
    chosen = []
    finished = float("-inf")
    for start, end in sorted(intervals):
        if start >= finished:
            chosen.append((start, end))
            finished = end
    return chosen

def by_shortest(intervals):
    """Take the shortest first. Also plausible, also wrong.

    A short interval can straddle the boundary between two longer ones and
    block both. On [(0,5), (4,6), (5,10)] the shortest is (4,6), which conflicts
    with both others, so this returns one where two fit.
    """
    chosen: list = []
    for start, end in sorted(intervals, key=lambda interval: interval[1] - interval[0]):
        if all(end <= other_start or start >= other_end for other_start, other_end in chosen):
            chosen.append((start, end))
    return sorted(chosen)
