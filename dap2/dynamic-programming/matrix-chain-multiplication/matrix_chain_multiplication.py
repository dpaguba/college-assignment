"""Matrix chain multiplication: where to put the brackets."""

from __future__ import annotations


def matrix_chain_order(dimensions):
    """Return the fewest scalar multiplications, and the bracketing that gives it.

    Matrix multiplication is associative, so the result never changes, and the
    cost changes enormously. Multiplying a 10x30 by a 30x5 by a 5x60:

        ((A1 A2) A3) costs 10·30·5 + 10·5·60 =  4500
        (A1 (A2 A3)) costs 30·5·60 + 10·30·60 = 27000

    Six times the work for the same answer. The problem is choosing the
    brackets, and the number of bracketings is the Catalan numbers, which grow
    faster than 2ⁿ.

    The recurrence is over **intervals** rather than prefixes, which is the new
    shape here. The best way to multiply the chain from i to j is: split it at
    some k, solve both halves, and pay for combining the two results. There are
    O(n²) intervals and each tries O(n) split points, giving O(n³).

    That interval shape reappears in optimal binary search trees, polygon
    triangulation and the CYK parsing algorithm, and it is the reason the loops
    below iterate by chain **length** rather than by position: a longer interval
    needs every shorter one to be ready.
    """
    if len(dimensions) < 2:
        raise ValueError("at least two dimensions are needed to have a matrix")

    count = len(dimensions) - 1
    cost = [[0] * count for _ in range(count)]
    split = [[0] * count for _ in range(count)]

    for length in range(2, count + 1):
        for start in range(count - length + 1):
            end = start + length - 1
            cost[start][end] = float("inf")
            for middle in range(start, end):
                candidate = (
                    cost[start][middle]
                    + cost[middle + 1][end]
                    + dimensions[start] * dimensions[middle + 1] * dimensions[end + 1]
                )
                if candidate < cost[start][end]:
                    cost[start][end] = candidate
                    split[start][end] = middle

    def brackets(start, end):
        """The bracketing of the range, read off the split table."""
        if start == end:
            return f"A{start + 1}"
        middle = split[start][end]
        return f"({brackets(start, middle)}{brackets(middle + 1, end)})"

    return cost[0][count - 1], brackets(0, count - 1)
