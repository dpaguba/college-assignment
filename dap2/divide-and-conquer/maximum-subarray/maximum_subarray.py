"""Maximum subarray by divide and conquer: the lecture version, next to Kadane's."""

from __future__ import annotations


def maximum_subarray_divide_and_conquer(values):
    """Return the largest contiguous sum and its range, in O(n log n).

    Split the array in half. The best run either lies entirely in the left
    half, entirely in the right, or **crosses the middle**. The first two are
    the same problem on smaller input; the third is the only new work.

    A crossing run is found greedily and in linear time: walk left from the
    middle keeping the best running total, then walk right, and add them. That
    gives T(n) = 2T(n/2) + O(n), which the Master theorem resolves to
    O(n log n), the same shape as merge sort.

    Kadane, in the dynamic programming folder, answers the same question in
    O(n). This version is here because the reasoning matters more than the
    result: "left, right, or crossing" is the template for every divide and
    conquer argument, and this is the smallest problem where the crossing case
    is not trivial.
    """
    if not values:
        raise ValueError("an empty array has no subarray to maximise")

    def crossing(low, middle, high):
        """The best range that crosses the midpoint."""
        best_left, total = float("-inf"), 0
        left_index = middle
        for index in range(middle, low - 1, -1):
            total += values[index]
            if total > best_left:
                best_left, left_index = total, index

        best_right, total = float("-inf"), 0
        right_index = middle + 1
        for index in range(middle + 1, high + 1):
            total += values[index]
            if total > best_right:
                best_right, right_index = total, index

        return best_left + best_right, left_index, right_index

    def solve(low, high):
        """The best range inside the given bounds."""
        if low == high:
            return values[low], low, high

        middle = (low + high) // 2
        return max(
            solve(low, middle),
            solve(middle + 1, high),
            crossing(low, middle, high),
            key=lambda answer: answer[0],
        )

    return solve(0, len(values) - 1)
