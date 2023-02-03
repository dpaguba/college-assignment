# Error detection

Three schemes with three exactly stated strengths.

**Parity** catches any odd number of flipped bits and misses every even number.
Verified both ways: it detects one flip and misses two, which is the most
common error after a single bit.

**The internet checksum** is a ones' complement sum with end-around carry, and
the checksum of a message together with its own checksum is **zero**. That
identity is the entire verification side of the algorithm.

**A CRC** divides the message as a polynomial over GF(2) by a generator and
appends the remainder. With a degree-4 generator it catches every single-bit
error and every burst of up to four bits, verified over every position of a
ten-bit message.

## Why the CRC is the one in hardware

Division without carries is exclusive or, so the whole algorithm is a shift
register and a few gates. That is why a CRC is computed at line rate and a
checksum is not, and why the strong check lives at the link layer and the weak
one at the transport layer.

A random error pattern passes a 32-bit CRC with probability `2^-32`, about one
in four billion, which is the number that makes a higher-layer checksum
arguably redundant and empirically still worth having.
