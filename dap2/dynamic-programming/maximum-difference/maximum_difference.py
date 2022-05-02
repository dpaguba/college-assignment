"""Maximum difference: the largest values[j] - values[i] with i before j."""

from __future__ import annotations


def max_difference(values):
    """One pass, remembering the smallest value seen so far.

    The pair has to be **in order**: the subtrahend must appear before the
    minuend. Without that constraint the answer would just be max minus min
    and the problem would be trivial. With it, `[100, 1, 5]` answers 4, not 99.

    Keep the smallest value seen so far and, at each position, ask what the
    profit would be if this were the later element. The best of those is the
    answer, in Θ(n) time and O(1) space.

    Note that the answer may be negative, and it should be: on a strictly
    falling sequence every ordered pair is a loss, and the least bad one is the
    correct answer. Clamping the result to zero silently changes the problem to
    "profit or no trade", which is a different question.
    """
    if len(values) < 2:
        return None

    smallest = values[0]
    best = values[1] - values[0]

    for value in values[1:]:
        best = max(best, value - smallest)
        smallest = min(smallest, value)

    return best


def max_difference_via_kadane(values):
    """The same answer as a maximum subarray problem, to show they are one problem.

    Take the consecutive differences d[i] = values[i+1] - values[i]. Any
    ordered pair (i, j) telescopes: values[j] - values[i] is exactly the sum of
    d[i..j-1]. So the maximum ordered difference is the maximum subarray sum of
    the difference array, and Kadane solves it.

    This is the useful direction of the reduction: two problems that look
    unrelated in a textbook are the same problem in different coordinates. The
    single pass above is Kadane with the subtraction inlined, which is why both
    are Θ(n) and both keep exactly one running value.

    The empty subarray is not allowed here, since a pair must consist of two
    distinct positions.
    """
    if len(values) < 2:
        return None

    differences = [second - first for first, second in zip(values, values[1:])]

    best = running = differences[0]
    for difference in differences[1:]:
        running = max(difference, running + difference)
        best = max(best, running)
    return best
