# IEEE 754 single precision

One sign bit, eight exponent bits in excess by 127, twenty-three significand
bits with an implicit leading one. Verified against the platform encoding for
every value tried, including `1.0` as `00111111100000000000000000000000`.

The exponent bias makes the encoded form compare like an integer, and the
implicit one buys a free bit of precision. Both are the reason the format looks
more complicated than it is.

## The consequences the exercises ask about

**The spacing is logarithmic.** The gap between representable numbers doubles
at every power of two: at 1.0 it is about 1.2e-07 and at 1024 it is 1024 times
larger. Relative error is roughly constant and absolute error is not.

**Addition is not associative.** `(1e10 + -1e10) + 1` is 1 and
`1e10 + (-1e10 + 1)` is 0, because the 1 is lost against 1e10. More precision
moves the threshold and does not remove the phenomenon.

**Most decimals are not representable.** A third is not, and neither is 0.1.

## The reserved exponents

All zeros and all ones are reserved, which is why the usable exponent range is
1 to 254:

| exponent | significand | meaning |
|---|---|---|
| 0 | 0 | zero |
| 0 | non-zero | **denormal** |
| 255 | 0 | infinity |
| 255 | non-zero | NaN |

Denormals fill the gap between zero and the smallest normal, which would
otherwise be far larger than the gap between the two smallest normals. They
cost precision and, on many processors, a great deal of time.
