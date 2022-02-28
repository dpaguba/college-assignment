"""Three definitions of the determinant, and why only one is computed.

The Leibniz formula sums over every permutation, the Laplace expansion
recurses over a row, and elimination triangulates the matrix. All three give
the same number and their costs differ by orders of magnitude: for a six by
six matrix the sum over permutations needs 3600 multiplications and the
elimination about 70.
"""

import itertools
import os
import sys
from fractions import Fraction

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..",
                                "gaussian-elimination"))
import gaussian_elimination as gauss


def determinant(matrix):
    """The determinant, computed by elimination."""
    rows = gauss.to_fractions(matrix)
    size = len(rows)
    sign = Fraction(1)
    result = Fraction(1)
    for column in range(size):
        pivot = next((index for index in range(column, size)
                      if rows[index][column] != 0), None)
        if pivot is None:
            return Fraction(0)
        if pivot != column:
            rows[column], rows[pivot] = rows[pivot], rows[column]
            sign = -sign
        result *= rows[column][column]
        for index in range(column + 1, size):
            factor = rows[index][column] / rows[column][column]
            if factor:
                rows[index] = [entry - factor * other
                               for entry, other in zip(rows[index], rows[column])]
    return sign * result


def leibniz(matrix):
    """The determinant as a signed sum over all permutations."""
    rows = gauss.to_fractions(matrix)
    size = len(rows)
    total = Fraction(0)
    for permutation in itertools.permutations(range(size)):
        product = Fraction(1)
        for row, column in enumerate(permutation):
            product *= rows[row][column]
        total += signature(permutation) * product
    return total


def signature(permutation):
    """The sign of a permutation, counted from its inversions."""
    inversions = sum(1 for left in range(len(permutation))
                     for right in range(left + 1, len(permutation))
                     if permutation[left] > permutation[right])
    return 1 if inversions % 2 == 0 else -1


def laplace(matrix, row=0):
    """The determinant by expanding along a row."""
    rows = gauss.to_fractions(matrix)
    size = len(rows)
    if size == 1:
        return rows[0][0]
    total = Fraction(0)
    for column in range(size):
        if rows[row][column] == 0:
            continue
        minor = [[entry for position, entry in enumerate(other) if position != column]
                 for index, other in enumerate(rows) if index != row]
        total += ((-1) ** (row + column)) * rows[row][column] * laplace(minor)
    return total


def operation_counts(size):
    """How many multiplications each method needs for a matrix of this size."""
    factorial = 1
    for value in range(2, size + 1):
        factorial *= value
    gauss_cost = sum((size - column) * (size - column - 1)
                     for column in range(size))
    return {"leibniz": factorial * (size - 1), "gauss": gauss_cost,
            "laplace": _laplace_cost(size)}


def _laplace_cost(size):
    """The multiplications the recursive expansion performs."""
    if size <= 1:
        return 0
    return size * (1 + _laplace_cost(size - 1))
