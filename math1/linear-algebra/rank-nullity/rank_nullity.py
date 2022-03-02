"""The dimension theorem: what a map loses and what it keeps add up.

The kernel measures what a map collapses and the image measures what it
reaches, and their dimensions sum to the dimension of the source. Everything
else in the chapter follows: a map between spaces of equal dimension is
injective exactly when it is surjective, and a map into a smaller space can
never be injective.
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..",
                                "gaussian-elimination"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "vector-spaces"))
import gaussian_elimination as gauss
import vector_spaces


def kernel_basis(matrix):
    """A basis of the vectors the matrix sends to zero."""
    solution = gauss.solve(matrix, [0] * len(matrix))
    return solution["kernel"]


def image_basis(matrix):
    """A basis of the space the matrix reaches."""
    columns = [[row[index] for row in matrix] for index in range(len(matrix[0]))]
    return vector_spaces.basis_of(columns)


def rank(matrix):
    """The dimension of the image."""
    return len(image_basis(matrix))


def nullity(matrix):
    """The dimension of the kernel."""
    return len(kernel_basis(matrix))


def homomorphism_theorem(matrix):
    """Whether the source dimension splits into kernel and image.

    The vector space version of the homomorphism theorem: the quotient by the
    kernel is isomorphic to the image, and for finite dimensions that is the
    same statement as the dimensions adding up.
    """
    return nullity(matrix) + rank(matrix) == len(matrix[0])


def is_injective(matrix):
    """Whether the kernel is trivial."""
    return nullity(matrix) == 0


def is_surjective(matrix):
    """Whether the image fills the target."""
    return rank(matrix) == len(matrix)


def is_bijective(matrix):
    """Both at once, which needs the dimensions to agree."""
    return is_injective(matrix) and is_surjective(matrix)
