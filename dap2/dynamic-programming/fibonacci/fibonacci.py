"""Fibonacci four ways: the same recurrence, four costs."""

from __future__ import annotations

from functools import lru_cache


def fibonacci_naive(n):
    """Straight from the definition, and unusable past about forty.

    F(n) = F(n-1) + F(n-2) reads exactly like the mathematics and costs
    O(φⁿ) calls, because F(n-2) is recomputed inside F(n-1) and again beside
    it, all the way down. Computing F(40) makes over three hundred million
    calls to compute at most forty distinct values.

    That gap between the number of calls and the number of distinct answers is
    the entire motivation for dynamic programming.
    """
    if n < 0:
        raise ValueError("Fibonacci is not defined for negative indices here")
    if n < 2:
        return n
    return fibonacci_naive(n - 1) + fibonacci_naive(n - 2)


def fibonacci_memoised(n, cache=None):
    """The same recursion with the answers remembered: top-down.

    One line of change, and the cost drops from exponential to linear, because
    each distinct subproblem is computed once and read thereafter.

    This is the top-down form: the recursion is written as it reads, and only
    the subproblems actually needed get computed. The price is stack depth,
    which is why n is bounded by the interpreter's recursion limit unless the
    call is unrolled.
    """
    if n < 0:
        raise ValueError("Fibonacci is not defined for negative indices here")
    if cache is None:
        cache = {}
    if n < 2:
        return n
    if n not in cache:
        cache[n] = fibonacci_memoised(n - 1, cache) + fibonacci_memoised(n - 2, cache)
    return cache[n]


def fibonacci_tabulated(n):
    """Fill a table from the bottom: no recursion, no stack.

    The same work in the other direction. Start from the base cases and build
    forward in an order where every value is ready when needed.

    Tabulation makes the fill order explicit, and seeing the order is what
    reveals the next optimisation: each value uses only the two before it.
    """
    if n < 0:
        raise ValueError("Fibonacci is not defined for negative indices here")
    if n < 2:
        return n

    table = [0] * (n + 1)
    table[1] = 1
    for index in range(2, n + 1):
        table[index] = table[index - 1] + table[index - 2]
    return table[n]


def fibonacci_rolling(n):
    """Keep two numbers instead of a table: O(1) space.

    Once the fill order is visible, the table is obviously wasteful: nothing
    older than two steps is ever read again. Dropping it costs nothing and
    removes the O(n) memory.

    That move, noticing which part of the table is still live, is the standard
    second step in every dynamic programming problem here. Knapsack, LCS and
    edit distance all shrink from a full grid to one or two rows the same way.
    """
    if n < 0:
        raise ValueError("Fibonacci is not defined for negative indices here")
    previous, current = 0, 1
    for _ in range(n):
        previous, current = current, previous + current
    return previous


def call_counts(n):
    """How many calls each version makes, which is the whole lesson."""
    naive = 0
    memoised = 0

    def count_naive(k):
        """The plain recursion, counting its own calls."""
        nonlocal naive
        naive += 1
        return k if k < 2 else count_naive(k - 1) + count_naive(k - 2)

    @lru_cache(maxsize=None)
    def count_memoised(k):
        """The memoised recursion, counting its own calls."""
        nonlocal memoised
        memoised += 1
        return k if k < 2 else count_memoised(k - 1) + count_memoised(k - 2)

    count_naive(n)
    count_memoised(n)
    return naive, memoised
