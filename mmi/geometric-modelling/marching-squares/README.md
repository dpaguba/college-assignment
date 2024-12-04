# Marching squares

Extracting a contour from a field known only at grid points. Classify the four
corners of each cell as above or below the level, look up which edges the
contour crosses, interpolate where. Sixteen patterns, and the table is the
algorithm.

## The interpolation is not a refinement

Placing the crossing at the midpoint of the edge instead of interpolating costs
one division and does not converge at all:

| grid | interpolated | midpoint |
|---|---|---|
| 17 x 17 | 0.74% | 2.58% |
| 33 x 33 | 0.18% | 3.05% |
| 65 x 65 | 0.048% | 3.53% |
| 129 x 129 | **0.012%** | **4.94%** |

as the error in the length of the unit circle's contour. The midpoint version
gets *worse* with resolution, because the error stops being dominated by the
cell size and starts being dominated by the systematic half-cell offset.

With interpolation the enclosed area converges too: 0.49%, 0.12%, 0.032%,
0.008% at 33, 65, 129 and 257 samples, against the exact `pi`.

## The saddle cases

Two of the sixteen patterns have opposite corners above the level and the other
two below, and both ways of connecting them fit the samples equally well. The
data genuinely does not decide it.

The tie-break here uses the average of the four corners as a stand-in for the
value at the cell centre, which keeps the higher region connected. Some rule is
needed, not because one answer is right, but because **neighbouring cells must
agree**: an inconsistent choice leaves gaps in a contour that should be closed.

## Closedness as the test

A level set of a continuous function separates the plane, so the contour of a
field with no boundary crossings is always closed. Checking that every endpoint
is shared by an even number of segments is therefore a real test, and it passes
for a circle, two circles and an ellipse.

For the hyperbola `xy = 0.15` it reports open, and correctly: all 4 unmatched
endpoints lie on the grid border, as do all 14 for `sin(3x)cos(3y) = 0.2`. The
contour leaves the sampled domain, which is not the same as being broken.

## Why the case table has to match the corner numbering

The table shipped here numbers corners bottom-left, bottom-right, top-right,
top-left, with edge `e` between corner `e` and `e+1`, so 0 bottom, 1 right,
2 top, 3 left. Written against a different edge numbering, with the geometry
unchanged, the contour length **diverged** with resolution (17.9%, 24.2%, 36.5%,
40.3% at 9, 33, 129, 257) and no contour was ever closed. It looked like a
subtle numerical problem and was a rotated lookup table.
