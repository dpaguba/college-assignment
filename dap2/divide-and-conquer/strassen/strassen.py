"""Strassen: multiplying matrices with seven block products instead of eight.

Below the cutoff the block bookkeeping costs more than the saved
multiplication.
"""

from __future__ import annotations

SMALL = 32

def naive_multiply(left, right):
    """The definition, three nested loops, O(n³)."""
    size = len(left)
    inner = len(right)
    columns = len(right[0])
    return [
        [sum(left[i][k] * right[k][j] for k in range(inner)) for j in range(columns)]
        for i in range(size)
    ]

def _add(a, b):
    """The sum of two matrices."""
    return [[x + y for x, y in zip(row_a, row_b)] for row_a, row_b in zip(a, b)]

def _subtract(a, b):
    """The difference of two matrices."""
    return [[x - y for x, y in zip(row_a, row_b)] for row_a, row_b in zip(a, b)]

def _split(matrix):
    """The four quarters of a matrix."""
    half = len(matrix) // 2
    top, bottom = matrix[:half], matrix[half:]
    return (
        [row[:half] for row in top], [row[half:] for row in top],
        [row[:half] for row in bottom], [row[half:] for row in bottom],
    )

def _pad(matrix, size):
    """The matrix padded with zeros to the given size."""
    padded = [row + [0] * (size - len(row)) for row in matrix]
    padded += [[0] * size for _ in range(size - len(matrix))]
    return padded

def strassen(left, right):
    """Return the matrix product, computed by divide and conquer.

    Splitting each matrix into four blocks turns one n×n product into eight
    products of half the size, which gives T(n) = 8T(n/2) + O(n²) and resolves
    to n³: no better than the definition. The recursion by itself buys nothing.

    Strassen's 1969 discovery is a set of seven products, each a combination of
    sums of blocks, from which all four result blocks can be assembled. Seven
    instead of eight changes the recurrence to T(n) = 7T(n/2) + O(n²), which
    the Master theorem resolves to n^log₂7, about n^2.807.

    The seven combinations look arbitrary and are not derived from anything
    intuitive, which is exactly why the result was a surprise: it showed that
    the obvious decomposition was not the only one, and it opened the search
    for lower exponents that is still running. The current record is around
    2.371, and none of those algorithms is practical.

    Strassen itself becomes practical from a few hundred rows, which is why
    real libraries switch to it above a threshold and use the plain method
    below it, exactly as this does.

    The block split needs an even size, so odd matrices are padded with zeros
    and the padding is trimmed off the result.
    """
    if len(left) != len(left[0]) or len(right) != len(right[0]) or len(left) != len(right):
        if len(left[0]) != len(right):
            raise ValueError("matrix sizes do not line up")

    size = len(left)
    if size <= SMALL or size == 1:
        return naive_multiply(left, right)

    if size % 2:
        padded = size + 1
        result = strassen(_pad(left, padded), _pad(right, padded))
        return [row[:size] for row in result[:size]]

    a, b, c, d = _split(left)
    e, f, g, h = _split(right)

    p1 = strassen(a, _subtract(f, h))
    p2 = strassen(_add(a, b), h)
    p3 = strassen(_add(c, d), e)
    p4 = strassen(d, _subtract(g, e))
    p5 = strassen(_add(a, d), _add(e, h))
    p6 = strassen(_subtract(b, d), _add(g, h))
    p7 = strassen(_subtract(a, c), _add(e, f))

    top_left = _add(_subtract(_add(p5, p4), p2), p6)
    top_right = _add(p1, p2)
    bottom_left = _add(p3, p4)
    bottom_right = _subtract(_subtract(_add(p5, p1), p3), p7)

    top = [left_row + right_row for left_row, right_row in zip(top_left, top_right)]
    bottom = [left_row + right_row for left_row, right_row in zip(bottom_left, bottom_right)]
    return top + bottom

def multiplication_counts(size):
    """How many block products one level of Strassen makes. Seven is the point."""
    calls = 0

    def counted(a, b, depth=0):
        """The counting wrapper, which records one call per multiplication."""
        nonlocal calls
        if depth == 1:
            calls += 1
            return naive_multiply(a, b)
        quarter_a = _split(a)
        quarter_b = _split(b)
        p, q, r, s = quarter_a
        e, f, g, h = quarter_b
        for pair in (
            (p, _subtract(f, h)), (_add(p, q), h), (_add(r, s), e), (s, _subtract(g, e)),
            (_add(p, s), _add(e, h)), (_subtract(q, s), _add(g, h)), (_subtract(p, r), _add(e, f)),
        ):
            counted(pair[0], pair[1], depth + 1)
        return None

    matrix = [[1] * size for _ in range(size)]
    counted(matrix, matrix)
    return calls
