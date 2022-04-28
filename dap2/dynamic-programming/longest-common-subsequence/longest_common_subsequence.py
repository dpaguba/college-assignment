"""Longest common subsequence: the longest order-preserving overlap of two sequences."""

from __future__ import annotations


def lcs_length(left, right):
    """The length of the longest common subsequence.

    A subsequence keeps the order but not the adjacency, so it is a far weaker
    requirement than a substring, and correspondingly harder to search for
    directly: there are 2ⁿ subsequences of a sequence.

    The recurrence compares one element from each end:

        if the last elements match, the answer is 1 + LCS of both prefixes
        otherwise it is the better of dropping one element from either side

    The grid is what makes it tractable. Two indices, one per sequence, so
    there are only n·m distinct subproblems, and each is one comparison and at
    most two lookups.

    This is the shape shared by edit distance and sequence alignment, and it is
    the same computation `diff` performs to decide which lines are unchanged.
    """
    rows, columns = len(left), len(right)
    table = [[0] * (columns + 1) for _ in range(rows + 1)]

    for row in range(1, rows + 1):
        for column in range(1, columns + 1):
            if left[row - 1] == right[column - 1]:
                table[row][column] = table[row - 1][column - 1] + 1
            else:
                table[row][column] = max(table[row - 1][column], table[row][column - 1])

    return table[rows][columns]


def lcs(left, right):
    """The subsequence itself, in the same type as the inputs.

    Rebuilding it means walking the table backwards from the corner: a match
    moves diagonally and contributes a character, otherwise the walk follows
    whichever neighbour holds the larger value.

    The path taken when the neighbours are equal is arbitrary, which is why
    several different subsequences of the same maximal length can be correct.
    """
    rows, columns = len(left), len(right)
    table = [[0] * (columns + 1) for _ in range(rows + 1)]

    for row in range(1, rows + 1):
        for column in range(1, columns + 1):
            if left[row - 1] == right[column - 1]:
                table[row][column] = table[row - 1][column - 1] + 1
            else:
                table[row][column] = max(table[row - 1][column], table[row][column - 1])

    result = []
    row, column = rows, columns
    while row > 0 and column > 0:
        if left[row - 1] == right[column - 1]:
            result.append(left[row - 1])
            row, column = row - 1, column - 1
        elif table[row - 1][column] >= table[row][column - 1]:
            row -= 1
        else:
            column -= 1

    result.reverse()
    return "".join(result) if isinstance(left, str) else result


def lcs_length_rolling(left, right):
    """The length using two rows instead of the whole grid.

    Each row reads only the row above and the cell to the left, so two rows are
    enough and the memory drops from n·m to min(n, m).

    The length survives the optimisation and the subsequence does not: the path
    that would be walked backwards lived in the rows that were discarded. That
    trade, answer or reconstruction, appears throughout this folder. Hirschberg's
    algorithm gets both, in linear space and twice the time, by recursing on the
    midpoint.
    """
    if len(right) > len(left):
        left, right = right, left

    previous = [0] * (len(right) + 1)
    for row in range(1, len(left) + 1):
        current = [0] * (len(right) + 1)
        for column in range(1, len(right) + 1):
            if left[row - 1] == right[column - 1]:
                current[column] = previous[column - 1] + 1
            else:
                current[column] = max(previous[column], current[column - 1])
        previous = current

    return previous[len(right)]
