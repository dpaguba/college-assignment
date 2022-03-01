"""Eigenvalues over the rationals, and the matrices that have none.

An eigenvector is a direction the map only stretches, and its eigenvalue is
the factor. The characteristic polynomial is built here in exact arithmetic,
so its coefficients are the trace and the determinant rather than
approximations of them, and the roots are searched for among the rationals
the rational root theorem allows.

Two failures are worth separating. A rotation has no real eigenvalue at all,
because no direction survives it. A shear has one eigenvalue and too few
eigenvectors, so it cannot be diagonalised even though its eigenvalue is
perfectly real.
"""

import os
import sys
from fractions import Fraction

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..",
                                "gaussian-elimination"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "determinants"))
import determinants
import gaussian_elimination as gauss


def trace(matrix):
    """The sum of the diagonal."""
    return sum(Fraction(matrix[index][index]) for index in range(len(matrix)))


def characteristic_polynomial(matrix):
    """The coefficients of det(A - xI), lowest degree first.

    Computed by interpolation: the determinant is evaluated at enough points
    and the polynomial through them is reconstructed exactly, which avoids
    writing a symbolic determinant and stays in exact arithmetic.
    """
    size = len(matrix)
    points = []
    for value in range(size + 1):
        shifted = [[Fraction(matrix[row][column]) - (Fraction(value)
                                                     if row == column else 0)
                    for column in range(size)] for row in range(size)]
        points.append((Fraction(value), determinants.determinant(shifted)))
    return _interpolate(points)


def _interpolate(points):
    """The coefficients of the polynomial through the given points."""
    size = len(points)
    matrix = [[point ** power for power in range(size)] for point, _ in points]
    values = [value for _, value in points]
    solution = gauss.solve(matrix, values)
    return solution["particular"]


def evaluate(polynomial, value):
    """The value of the polynomial at a point."""
    total = Fraction(0)
    for power, coefficient in enumerate(polynomial):
        total += coefficient * Fraction(value) ** power
    return total


def rational_eigenvalues(matrix):
    """Every rational root of the characteristic polynomial.

    Searched over the candidates the rational root theorem allows, so the
    result is complete for rational eigenvalues and says nothing about the
    irrational or complex ones, which is the exact scope of the method.
    """
    polynomial = characteristic_polynomial(matrix)
    while polynomial and polynomial[-1] == 0:
        polynomial = polynomial[:-1]
    if not polynomial:
        return []
    denominator = 1
    for coefficient in polynomial:
        denominator = denominator * coefficient.denominator // _gcd(
            denominator, coefficient.denominator)
    integers = [int(coefficient * denominator) for coefficient in polynomial]
    constant, leading = integers[0], integers[-1]
    found = []
    for numerator in _divisors(abs(constant) or 1):
        for divisor in _divisors(abs(leading)):
            for sign in (1, -1):
                candidate = Fraction(sign * numerator, divisor)
                if candidate in found:
                    continue
                if evaluate(polynomial, candidate) == 0:
                    found.append(candidate)
    if constant == 0 and Fraction(0) not in found:
        found.append(Fraction(0))
    return sorted(found)


def _divisors(value):
    """Every positive divisor of the value."""
    return [candidate for candidate in range(1, abs(value) + 1)
            if value % candidate == 0]


def _gcd(first, second):
    """The greatest common divisor."""
    while second:
        first, second = second, first % second
    return first


def eigenvectors(matrix, value):
    """A basis of the eigenspace of the given eigenvalue."""
    size = len(matrix)
    shifted = [[Fraction(matrix[row][column]) - (value if row == column else 0)
                for column in range(size)] for row in range(size)]
    return gauss.solve(shifted, [0] * size)["kernel"]


def is_diagonalisable(matrix):
    """Whether the eigenvectors span the whole space."""
    vectors = []
    for value in rational_eigenvalues(matrix):
        vectors.extend(eigenvectors(matrix, value))
    if not vectors:
        return False
    return gauss.rank(vectors) == len(matrix)


def algebraic_multiplicity(matrix, value):
    """How often the eigenvalue is a root of the characteristic polynomial."""
    polynomial = characteristic_polynomial(matrix)
    count = 0
    while polynomial and evaluate(polynomial, value) == 0:
        polynomial = _divide(polynomial, value)
        count += 1
    return count


def _divide(polynomial, root):
    """The polynomial divided by x minus the root, by synthetic division."""
    coefficients = list(reversed(polynomial))
    result = [coefficients[0]]
    for coefficient in coefficients[1:]:
        result.append(coefficient + result[-1] * root)
    return list(reversed(result[:-1]))


def geometric_multiplicity(matrix, value):
    """The dimension of the eigenspace."""
    return len(eigenvectors(matrix, value))
