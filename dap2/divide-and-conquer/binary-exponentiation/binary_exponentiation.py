"""Binary exponentiation: a power in log n multiplications instead of n."""

from __future__ import annotations


def power(base, exponent):
    """Return base to the exponent, using O(log n) multiplications.

    Multiplying by the base n times costs n multiplications. Squaring costs
    log₂(n), because each squaring doubles the exponent reached:
    x² gives x⁴ gives x⁸, and the binary digits of n say which of those to keep.

    x^13 with 13 = 1101 in binary is x^8 · x^4 · x^1: three multiplications
    from the squarings and two to combine, against twelve for the naive loop.

    It is divide and conquer in its smallest form, x^n = (x^(n/2))², and the
    reason it matters far beyond arithmetic: the same halving works for
    anything associative. Matrices, permutations, polynomials, group elements.
    """
    if exponent < 0:
        raise ValueError("negative exponents need division, which integers lack")

    result = 1
    while exponent:
        if exponent & 1:
            result *= base
        base *= base
        exponent >>= 1
    return result


def power_mod(base, exponent, modulus):
    """The same, reducing at every step so the numbers stay small.

    Computing 7^1000 and then taking the remainder means holding a number with
    850 digits. Reducing after every multiplication keeps everything below the
    modulus squared, and the answer is identical because modular arithmetic
    commutes with multiplication.

    This is the operation RSA and Diffie-Hellman are built from, and the reason
    public key cryptography is possible at all: the exponent can be astronomical
    while the work stays logarithmic.
    """
    if exponent < 0:
        raise ValueError("negative exponents need a modular inverse")
    if modulus == 1:
        return 0

    result = 1
    base %= modulus
    while exponent:
        if exponent & 1:
            result = result * base % modulus
        base = base * base % modulus
        exponent >>= 1
    return result


def matrix_power(matrix, exponent):
    """The same halving applied to matrices.

    Because it needs only associativity, the algorithm transfers unchanged. The
    Fibonacci matrix [[1,1],[1,0]] raised to n holds F(n) in its corner, which
    computes Fibonacci in O(log n) multiplications rather than the O(n)
    additions of the usual loop.

    That is the payoff of noticing what an algorithm actually depends on:
    binary exponentiation never needed numbers, only a way to combine two
    things that does not care about grouping.
    """
    if exponent < 0:
        raise ValueError("negative exponents need a matrix inverse")

    size = len(matrix)
    result = [[1 if i == j else 0 for j in range(size)] for i in range(size)]

    def multiply(left, right):
        """The product of two matrices."""
        return [
            [sum(left[i][k] * right[k][j] for k in range(size)) for j in range(size)]
            for i in range(size)
        ]

    while exponent:
        if exponent & 1:
            result = multiply(result, matrix)
        matrix = multiply(matrix, matrix)
        exponent >>= 1
    return result


def multiplication_count(base, exponent):
    """How many multiplications the method actually performs."""
    count = 0
    while exponent:
        if exponent & 1:
            count += 1
        count += 1
        exponent >>= 1
    return count
