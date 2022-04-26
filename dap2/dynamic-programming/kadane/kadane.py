"""Kadane's algorithm: the best contiguous run, in one pass."""

from __future__ import annotations

def maximum_subarray(values):
    """Return the largest sum of a contiguous run, and where it sits.

    The brute force is O(n²): every start against every end. Divide and conquer
    brings it to O(n log n) by splitting and handling the runs that cross the
    middle, and that version is the standard example in the divide and conquer
    lecture.

    Kadane does it in one pass by asking a smaller question. For each position,
    what is the best run **ending here**? There are only two candidates: this
    element alone, or this element added to the best run ending at the previous
    position. The choice is one comparison, and the answer to the whole problem
    is the best of those n answers.

    That reframing, from "best run anywhere" to "best run ending here", is the
    move that turns a search into a recurrence. It reappears throughout dynamic
    programming: the state has to be something a single step can extend.

    All-negative input is where naive versions break, because they initialise
    the running total to zero and then report zero for an array that has no
    empty run. Starting from the first element instead is the fix.
    """
    if not values:
        raise ValueError("an empty array has no subarray to maximise")

    best = current = values[0]
    best_start = best_end = current_start = 0

    for index in range(1, len(values)):
        value = values[index]
        if current + value < value:
            current, current_start = value, index
        else:
            current += value

        if current > best:
            best, best_start, best_end = current, current_start, index

    return best, best_start, best_end
