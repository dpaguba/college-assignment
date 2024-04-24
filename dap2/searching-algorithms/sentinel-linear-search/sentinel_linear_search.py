"""Sentinel linear search: put the target at the end so the loop needs one test."""

from __future__ import annotations

def sentinel_linear_search(items, target, key=None):
    """Return the index of `target`, or -1 if it is not there.

    Plain linear search checks two things per step: have I found it, and have I
    run off the end. Appending the target as a sentinel guarantees the first
    check eventually succeeds, so the bounds test can be dropped from the loop
    entirely and reappears once, after it.

    Halving the comparisons per iteration changes no complexity at all and used
    to be worth real time in tight loops. It is here as the clearest example of
    a constant-factor optimisation, the kind big-O deliberately ignores and a
    profiler does not.

    The array is copied rather than appended to, because a search has no
    business modifying what it was given.
    """
    of = key or (lambda item: item)
    if not items:
        return -1

    probe = list(items)
    last = len(probe) - 1
    final_value = probe[last]
    probe[last] = target if key is None else items[last]

    index = 0
    if key is None:
        while probe[index] != target:
            index += 1
    else:
        while index < last and of(probe[index]) != target:
            index += 1

    if index < last:
        return index
    return last if of(final_value) == target else -1
