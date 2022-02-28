# Determinants

Three definitions, one number, and costs that differ by orders of magnitude.

Multiplications needed:

| size | Leibniz (all permutations) | Laplace (recursive) | Gauss |
|---|---:|---:|---:|
| 4 | 72 | 40 | 20 |
| 6 | 3 600 | 1 236 | 70 |
| 8 | 282 240 | 69 280 | 168 |

All three are implemented and all three agree on every matrix tested, which
is the point of implementing the expensive ones: the cheap method is trusted
because it matches the definition, not because the definition is unusable.

The gap grows factorially. At size 8 the sum over permutations needs 1600
times the work of elimination, and elimination is what any library does,
including the one this module is checked against.

## What the number means

The determinant is zero exactly when the matrix is singular, which is checked
here against the inverse existing. It is multiplicative, so the determinant of
a product is the product of the determinants, which is why it is invariant
under a change of basis and can be attached to a map rather than a matrix.

Swapping two rows changes the sign, which is the one property that makes the
Leibniz formula's alternating sign necessary rather than decorative.

Verified against numpy on 300 random matrices.
