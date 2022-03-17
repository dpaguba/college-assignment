"""Multipliers: shift and add, arrays, and Booth's recoding.

Multiplication is repeated addition of shifted copies, and the three designs
differ in when the additions happen. Shift and add does one per cycle; an array
multiplier does them all at once in a grid of adders; Booth's algorithm reduces
how many are needed at all.

Booth's insight is that a run of ones can be rewritten:
`0111 = 1000 - 1`, so eight minus one replaces three additions with one
addition and one subtraction. The saving grows with the length of the run,
which is why the algorithm exists and why it also handles signed operands
without a special case.
"""

from __future__ import annotations


def shift_and_add(left, right, bits):
    """The sequential algorithm: one shifted addition per set bit."""
    result = 0

    for position in range(bits):
        if (right >> position) & 1:
            result += left << position

    return result


def shift_and_add_steps(multiplier, bits):
    """How many additions the sequential algorithm performs.

    One per set bit, so the cost depends on the operand rather than only on the
    width. A multiplier of all ones is the worst case, which is exactly the
    case Booth's recoding turns into the best one.
    """
    return sum(1 for position in range(bits) if (multiplier >> position) & 1)


def array_multiply(left, right, bits):
    """The combinational form: every partial product at once.

    Area grows with the square of the width and delay with the width, which is
    the opposite trade from the sequential version. Modern designs use a
    Wallace tree to bring the delay down to logarithmic at the cost of an
    irregular layout.
    """
    partials = [(left if (right >> position) & 1 else 0) << position
                for position in range(bits)]
    return sum(partials)


def booth_recode(multiplier, bits):
    """Booth's recoding: each digit becomes -1, 0 or +1.

    Read the multiplier two bits at a time with an implicit zero below, and
    emit a subtraction where a run of ones begins and an addition where it
    ends. A run of `k` ones costs two operations instead of `k`.

    The digit at position `i` is `y[i-1] - y[i]`, and summing `digit * M * 2^i`
    over every position gives the product with **no** correction term for a
    negative multiplier. The telescoping sum works out to the two's complement
    value of the multiplier, which is why the algorithm handles signed operands
    for free rather than as an extra case.
    """
    digits = []
    previous = 0

    for position in range(bits):
        current = (multiplier >> position) & 1
        digits.append(previous - current)
        previous = current

    return digits


def booth(left, right, bits):
    """Multiply two signed values using Booth's recoding."""
    mask = (1 << bits) - 1
    encoded = right & mask
    digits = booth_recode(encoded, bits)

    result = 0
    for position, digit in enumerate(digits):
        result += digit * (left << position)

    return result


def booth_steps(multiplier, bits):
    """How many additions or subtractions Booth's algorithm performs."""
    return sum(1 for digit in booth_recode(multiplier, bits) if digit != 0)


def partial_product_count(bits):
    """How many rows an array multiplier has to sum."""
    return bits


def wallace_depth(bits):
    """Depth of a Wallace tree reduction, in full-adder levels.

    Each level reduces three rows to two, so the number of rows falls by a
    factor of 1.5 per level and the depth is logarithmic. That is the
    difference between a multiplier that fits in one cycle and one that does
    not.
    """
    rows = bits
    depth = 0

    while rows > 2:
        rows = (rows // 3) * 2 + rows % 3
        depth += 1

    return depth
