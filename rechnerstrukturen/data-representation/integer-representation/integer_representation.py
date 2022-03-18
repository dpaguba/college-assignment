"""Four ways to write a signed integer in a fixed number of bits.

All four agree on non-negative numbers and disagree on everything else, which
is why the exercise asks for the same value in all of them.

| representation | negative numbers | zeros | range in 8 bits |
|---|---|---|---|
| sign and magnitude | flip the top bit | **two** | -127 to 127 |
| ones' complement | invert every bit | **two** | -127 to 127 |
| two's complement | invert and add one | one | -128 to 127 |
| excess by bias | store value plus bias | one | -bias to 255-bias |

Two's complement won because addition needs no case distinction: the same adder
that computes `3 + 5` computes `3 + (-5)`, and the carry out is simply
discarded. Every other representation needs the sign inspected first.
"""

from __future__ import annotations


def encode(value, bits, form, bias=None):
    """The bit pattern for a value in one representation."""
    if form == "sign-magnitude":
        sign = 1 if value < 0 else 0
        magnitude = abs(value)
        return f"{sign}{magnitude:0{bits - 1}b}"

    if form == "ones-complement":
        if value >= 0:
            return format(value, f"0{bits}b")
        return "".join("1" if character == "0" else "0"
                       for character in format(-value, f"0{bits}b"))

    if form == "twos-complement":
        return format(value & ((1 << bits) - 1), f"0{bits}b")

    if form == "excess":
        if bias is None:
            bias = (1 << (bits - 1)) - 1
        return format(value + bias, f"0{bits}b")

    raise ValueError(f"unknown representation {form}")


def decode(pattern, form, bias=None):
    """The value a bit pattern denotes in one representation."""
    bits = len(pattern)
    raw = int(pattern, 2)

    if form == "sign-magnitude":
        magnitude = int(pattern[1:], 2)
        return -magnitude if pattern[0] == "1" else magnitude

    if form == "ones-complement":
        if pattern[0] == "0":
            return raw
        inverted = "".join("1" if character == "0" else "0" for character in pattern)
        return -int(inverted, 2)

    if form == "twos-complement":
        return raw - (1 << bits) if pattern[0] == "1" else raw

    if form == "excess":
        if bias is None:
            bias = (1 << (bits - 1)) - 1
        return raw - bias

    raise ValueError(f"unknown representation {form}")


def value_range(bits, form, bias=None):
    """The smallest and largest value a representation can hold."""
    if form == "twos-complement":
        return (-(1 << (bits - 1)), (1 << (bits - 1)) - 1)
    if form in ("sign-magnitude", "ones-complement"):
        limit = (1 << (bits - 1)) - 1
        return (-limit, limit)
    if form == "excess":
        if bias is None:
            bias = (1 << (bits - 1)) - 1
        return (-bias, (1 << bits) - 1 - bias)
    raise ValueError(f"unknown representation {form}")


def zeros(bits, form):
    """The bit patterns that denote zero.

    Two of them in sign-magnitude and ones' complement, which is the practical
    objection to both: every comparison against zero needs two tests, and one
    bit pattern out of the range is wasted.
    """
    return [format(value, f"0{bits}b") for value in range(1 << bits)
            if decode(format(value, f"0{bits}b"), form) == 0]


def add(left, right, bits, form):
    """Add two values in a representation, reporting overflow.

    In two's complement the addition is the unsigned one with the carry
    discarded, and overflow is detected by the two operands agreeing in sign
    while the result disagrees. In ones' complement a carry out has to be added
    back in, the end-around carry, which is the extra hardware two's complement
    avoids.
    """
    modulus = 1 << bits

    if form == "twos-complement":
        raw = (left + right) % modulus
        value = raw - modulus if raw >= modulus // 2 else raw
        overflow = (left >= 0) == (right >= 0) and (value >= 0) != (left >= 0)
        return {"value": value, "overflow": overflow,
                "pattern": format(raw, f"0{bits}b")}

    if form == "ones-complement":
        raw = int(encode(left, bits, form), 2) + int(encode(right, bits, form), 2)
        if raw >= modulus:
            raw = (raw % modulus) + 1
        value = decode(format(raw % modulus, f"0{bits}b"), form)
        low, high = value_range(bits, form)
        return {"value": value, "overflow": not low <= left + right <= high,
                "pattern": format(raw % modulus, f"0{bits}b")}

    low, high = value_range(bits, form)
    total = left + right
    return {"value": total, "overflow": not low <= total <= high,
            "pattern": encode(total, bits, form) if low <= total <= high else None}


def negate(pattern, form):
    """The pattern of the negated value."""
    bits = len(pattern)
    return encode(-decode(pattern, form), bits, form)
