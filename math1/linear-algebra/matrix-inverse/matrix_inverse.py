"""Inverting a matrix, and writing it as a product of elementary ones.

Gauss-Jordan on the matrix beside the identity performs the same row
operations on both, so what leaves as the second half is the inverse. Each
row operation is itself a matrix, which is why an invertible matrix is a
product of elementary matrices: the elimination is the factorisation.
"""

import os
import sys
from fractions import Fraction

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..",
                                "gaussian-elimination"))
import gaussian_elimination as gauss


def identity(size):
    """The identity matrix of the given size."""
    return [[Fraction(1) if row == column else Fraction(0)
             for column in range(size)] for row in range(size)]


def multiply(first, second):
    """The matrix product."""
    left = gauss.to_fractions(first)
    right = gauss.to_fractions(second)
    return [[sum(left[row][index] * right[index][column]
                 for index in range(len(right)))
             for column in range(len(right[0]))] for row in range(len(left))]


def inverse(matrix):
    """The inverse, or nothing when the matrix is singular."""
    size = len(matrix)
    rows = [list(row) + identity(size)[index]
            for index, row in enumerate(gauss.to_fractions(matrix))]
    reduced = gauss.reduced_row_echelon(rows)
    left = [row[:size] for row in reduced]
    if left != identity(size):
        return None
    return [row[size:] for row in reduced]


def swap_matrix(size, first, second):
    """The elementary matrix that exchanges two rows."""
    result = identity(size)
    result[first], result[second] = result[second], result[first]
    return result


def scale_matrix(size, row, factor):
    """The elementary matrix that multiplies one row."""
    result = identity(size)
    result[row][row] = Fraction(factor)
    return result


def add_matrix(size, target, source, factor):
    """The elementary matrix that adds a multiple of one row to another."""
    result = identity(size)
    result[target][source] = Fraction(factor)
    return result


def as_elementary_product(matrix):
    """The matrix as a product of elementary matrices, or nothing.

    The elimination applies E1 up to Ek and reaches the identity, so the
    matrix is the product of their inverses in the same order. That is the
    factorisation: every step of Gauss-Jordan is one elementary factor.
    """
    size = len(matrix)
    rows = gauss.to_fractions(matrix)
    operations = []
    pivot_row = 0
    for column in range(size):
        pivot = next((index for index in range(pivot_row, size)
                      if rows[index][column] != 0), None)
        if pivot is None:
            return None
        if pivot != pivot_row:
            rows[pivot_row], rows[pivot] = rows[pivot], rows[pivot_row]
            operations.append(swap_matrix(size, pivot_row, pivot))
        factor = rows[pivot_row][column]
        if factor != 1:
            rows[pivot_row] = [entry / factor for entry in rows[pivot_row]]
            operations.append(scale_matrix(size, pivot_row, Fraction(1) / factor))
        for index in range(size):
            if index == pivot_row or rows[index][column] == 0:
                continue
            multiplier = rows[index][column]
            rows[index] = [entry - multiplier * other
                           for entry, other in zip(rows[index], rows[pivot_row])]
            operations.append(add_matrix(size, index, pivot_row, -multiplier))
        pivot_row += 1
    return [inverse(operation) for operation in operations]
