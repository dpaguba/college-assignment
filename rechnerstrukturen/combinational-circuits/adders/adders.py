"""Adders: the carry is the whole problem.

Each bit's sum is easy and its carry depends on every bit below it. A ripple
carry adder waits for that chain, so its delay grows linearly with the width; a
carry-lookahead adder computes the carries in parallel from generate and
propagate signals, so its delay grows logarithmically and its area grows
faster.

    g_i = a_i and b_i          this position generates a carry
    p_i = a_i xor b_i          this position passes one through

    c_(i+1) = g_i or (p_i and c_i)

Unrolling that recurrence is the whole trick: every carry becomes a two-level
expression in the generates and propagates, computable at once.
"""

from __future__ import annotations

import math


def full_adder(first, second, carry_in):
    """One bit of addition: the sum bit and the carry out."""
    total = first + second + carry_in
    return total % 2, total // 2


def generate(first, second):
    """Whether a position produces a carry regardless of the one below."""
    return first & second


def propagate(first, second):
    """Whether a position passes an incoming carry onwards."""
    return first ^ second


def ripple_carry(left, right, bits):
    """Add by chaining full adders, carry by carry."""
    carry = 0
    result = 0

    for position in range(bits):
        first = (left >> position) & 1
        second = (right >> position) & 1
        total, carry = full_adder(first, second, carry)
        result |= total << position

    return {"value": result, "carry": carry}


def ripple_delay(bits, gate_delay=2):
    """Delay of a ripple carry adder, in gate delays.

    Two gate delays per bit for the carry chain, so 32 bits cost 64. That
    number is why a processor's clock period was once set by its adder.
    """
    return bits * gate_delay


def carry_lookahead(left, right, bits):
    """Add by computing every carry from the generate and propagate signals.

    The carries are computed directly rather than passed along, so the
    arithmetic is identical and the timing is not. Comparing the two on every
    input is the check that matters: an adder that is fast and occasionally
    wrong is worse than a slow one.
    """
    generates = [generate((left >> position) & 1, (right >> position) & 1)
                 for position in range(bits)]
    propagates = [propagate((left >> position) & 1, (right >> position) & 1)
                  for position in range(bits)]

    carries = [0]
    for position in range(bits):
        carry = generates[position]
        product = propagates[position]
        for lower in range(position - 1, -1, -1):
            carry |= product & generates[lower]
            product &= propagates[lower]
        carries.append(carry)

    result = 0
    for position in range(bits):
        result |= (propagates[position] ^ carries[position]) << position

    return {"value": result, "carry": carries[bits]}


def lookahead_delay(bits, group=4, gate_delay=2):
    """Delay of a carry-lookahead adder built from groups.

    A single flat lookahead over 32 bits would need a 32-input gate, which no
    process provides, so real designs build a tree of small lookahead blocks.
    The delay is then logarithmic in the width with the group size as the base.
    """
    return gate_delay * (2 + math.ceil(math.log(bits, group)))


def subtract(left, right, bits):
    """Subtract by adding the two's complement.

    The same adder, with the second operand inverted and the carry in set. That
    is why an ALU has one adder and not two, and why two's complement is the
    representation everything uses.
    """
    inverted = ~right & ((1 << bits) - 1)
    carry = 1
    result = 0

    for position in range(bits):
        first = (left >> position) & 1
        second = (inverted >> position) & 1
        total, carry = full_adder(first, second, carry)
        result |= total << position

    return {"value": result, "carry": carry}


def carry_select_delay(bits, blocks, gate_delay=2):
    """Delay of a carry-select adder, which trades area for time.

    Each block computes both possible sums, for carry in zero and one, and a
    multiplexer picks when the real carry arrives. Twice the adders and roughly
    the square root of the delay, which is the middle point between ripple and
    full lookahead.
    """
    per_block = bits // blocks
    return gate_delay * (per_block + blocks)
