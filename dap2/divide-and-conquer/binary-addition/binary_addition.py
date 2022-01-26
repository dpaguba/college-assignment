"""Binary addition on bit arrays: the linear-time primitive everything else is measured against."""

from __future__ import annotations


def to_bits(number):
    """A non-negative integer as a list of bits, most significant first."""
    if number == 0:
        return [0]
    bits = []
    while number:
        bits.append(number & 1)
        number >>= 1
    return bits[::-1]


def to_int(bits):
    """A bit list back into an integer."""
    value = 0
    for bit in bits:
        value = value * 2 + bit
    return value


def add(first, second):
    """Add two bit arrays, most significant bit first, without converting to int.

    Schoolbook ripple-carry addition: walk both operands from the least
    significant end, add the two bits and the incoming carry, keep the low bit
    and pass the high one on.

    The point of doing it this way is that the cost is visible. Adding two
    n-bit numbers costs Θ(n) bit operations, and that is the baseline against
    which every other arithmetic algorithm in this folder is stated. Converting
    the operands to Python ints and using `+` gives the right answer while
    hiding the only thing the exercise is about.

    Θ(n) is also optimal: every input bit has to be read at least once, since
    flipping any one of them changes the answer.
    """
    result = []
    carry = 0
    i, j = len(first) - 1, len(second) - 1

    while i >= 0 or j >= 0 or carry:
        total = carry
        if i >= 0:
            total += first[i]
            i -= 1
        if j >= 0:
            total += second[j]
            j -= 1
        result.append(total & 1)
        carry = total >> 1

    result.reverse()
    return result or [0]
