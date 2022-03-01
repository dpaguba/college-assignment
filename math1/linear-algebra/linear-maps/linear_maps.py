"""Linear maps and their matrices, which depend on the bases chosen.

A linear map is determined by what it does to a basis, so a matrix is a map
written down with respect to two bases. Changing either basis changes the
matrix and not the map, which is why the quantities that describe the map
itself, its rank, its determinant, its eigenvalues, are the ones that survive
a change of basis.
"""

import os
import sys
from fractions import Fraction

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..",
                                "gaussian-elimination"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "matrix-inverse"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "vector-spaces"))
import gaussian_elimination as gauss
import matrix_inverse
import vector_spaces


def apply(matrix, vector):
    """The image of a vector under the matrix."""
    rows = gauss.to_fractions(matrix)
    return [sum(entry * value for entry, value in zip(row, vector)) for row in rows]


def matrix_of(function, source_basis, target_basis):
    """The matrix of a map, columns being the images of the source basis.

    Each image is written in the target basis, so the column entries are
    coordinates rather than components. With the standard bases the two
    coincide, which is why the distinction is easy to miss until the basis
    changes.
    """
    columns = []
    for vector in source_basis:
        image = function(vector)
        coordinates = vector_spaces.coordinates(target_basis, image)
        if coordinates is None:
            raise ValueError("the image is outside the span of the target basis")
        columns.append(coordinates)
    return [[columns[column][row] for column in range(len(columns))]
            for row in range(len(columns[0]))]


def compose(second, first):
    """The matrix of the composed map, which is the product."""
    return matrix_inverse.multiply(second, first)


def change_of_basis(old_basis, new_basis):
    """The matrix taking coordinates in the old basis to the new one."""
    return matrix_of(lambda vector: vector, old_basis, new_basis)


def in_basis(matrix, basis):
    """The same map written in another basis, by conjugation."""
    standard = [[Fraction(1) if row == column else Fraction(0)
                 for column in range(len(basis))] for row in range(len(basis))]
    change = change_of_basis(basis, standard)
    back = matrix_inverse.inverse(change)
    if back is None:
        raise ValueError("the basis is not a basis")
    return matrix_inverse.multiply(back, matrix_inverse.multiply(matrix, change))


def is_linear(function, dimension, samples=None):
    """Whether the function respects sums and scalar multiples on samples."""
    samples = samples or [[Fraction(value == index) for value in range(dimension)]
                          for index in range(dimension)]
    for first in samples:
        for second in samples:
            total = [a + b for a, b in zip(first, second)]
            if function(total) != [a + b for a, b in zip(function(first),
                                                         function(second))]:
                return False
        scaled = [Fraction(3) * entry for entry in first]
        if function(scaled) != [Fraction(3) * entry for entry in function(first)]:
            return False
    return True
