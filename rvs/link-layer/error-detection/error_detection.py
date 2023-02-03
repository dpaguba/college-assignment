"""Error detection: parity, checksums and cyclic redundancy checks.

Three schemes with three strengths, and the differences are exact rather than
vague.

**Parity** catches any odd number of flipped bits and misses every even number,
so it misses the two-bit error, which is the most common one after the
single-bit error.

**The internet checksum** adds the data in 16-bit words with end-around carry.
It catches more, it is cheap enough to compute in software, and it misses any
error whose changes cancel in the sum.

**A CRC** treats the message as a polynomial over GF(2) and appends the
remainder after division by a generator. With a generator of degree `r` it
catches every single-bit error, every burst shorter than or equal to `r`, and
every odd number of errors when the generator has a factor of `x + 1`.
"""

from __future__ import annotations


def parity_bit(bits):
    """The even parity bit of a bit sequence."""
    return sum(bits) % 2


def parity_detects(bits, flip):
    """Whether parity notices a given set of flipped positions."""
    original = parity_bit(bits)
    corrupted = list(bits)

    for position in flip:
        corrupted[position] ^= 1

    return parity_bit(corrupted) != original


def internet_checksum(words):
    """The ones' complement sum of 16-bit words, complemented.

    Carries are added back in, which is what makes it the ones' complement sum
    rather than an ordinary one, and it is why the checksum of a message
    together with its own checksum is zero. That property is the whole
    implementation of the verification side.
    """
    total = 0

    for word in words:
        total += word
        total = (total & 0xFFFF) + (total >> 16)

    return (~total) & 0xFFFF


def remainder(bits, generator):
    """The remainder of polynomial division over GF(2).

    Division without carries: subtraction is exclusive or, so the whole
    algorithm is a shift register and a few gates. That cheapness is why CRCs
    are computed in hardware at line rate while checksums are not.
    """
    work = list(bits)
    degree = len(generator) - 1

    for position in range(len(bits) - degree):
        if work[position] == 0:
            continue
        for offset, coefficient in enumerate(generator):
            work[position + offset] ^= coefficient

    return work[-degree:]


def crc(message, generator):
    """The check bits to append to a message."""
    degree = len(generator) - 1
    return remainder(list(message) + [0] * degree, generator)


def crc_detects(message, generator, flip):
    """Whether a CRC notices a given set of flipped positions."""
    degree = len(generator) - 1
    frame = list(message) + crc(message, generator)

    corrupted = list(frame)
    for position in flip:
        corrupted[position] ^= 1

    return any(remainder(corrupted, generator))


def burst_length_detected(generator):
    """The longest burst a generator is guaranteed to catch.

    Equal to its degree. A burst longer than that can coincide with a multiple
    of the generator and slip through, which is why the standard polynomials
    are 32 bits: it bounds the undetected burst to something longer than any
    plausible interference.
    """
    return len(generator) - 1


def undetected_probability(bits, random_errors=True):
    """The chance a random error pattern passes a check of a given width.

    `2^-r` for a CRC of degree `r`, because a random remainder is uniform. For
    32 bits that is one in four billion, which is the number that makes a
    checksum at a higher layer arguably redundant and empirically not.
    """
    return 2.0 ** (-bits)
