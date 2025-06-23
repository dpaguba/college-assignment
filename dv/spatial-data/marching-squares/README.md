# Marching squares

Each cell's four corner signs give a number from 0 to 15, and the number says
which edges the contour crosses. The crossing point on an edge is found by
linear interpolation of the two corner values.

On the unit circle x² + y² − 1 = 0 the contour comes out closed, on grids of
5, 6, 8, 11 and 14 points per axis, and every vertex lies within 0.056 cell
widths of the true circle.

## The exercise's rounding

The exercise asks for the division ratio to be rounded to one decimal before
drawing. That is fine on paper and it puts a floor under the accuracy:

| grid | exact | rounded |
|---|---|---|
| 5 | 0.0556 | 0.0395 |
| 7 | 0.0282 | 0.0139 |
| 9 | 0.0173 | 0.0250 |
| 13 | 0.0077 | 0.0139 |
| 21 | 0.0028 | 0.0100 |

The exact error keeps falling as the grid is refined; the rounded one stops.
By 21 points per axis the rounding is three and a half times worse than the
interpolation it replaces.

## Ambiguity

Cases 5 and 10 have the two positive corners diagonally opposite, and the
signs alone do not say whether the contour separates them or joins them. The
asymptotic decider evaluates the saddle point of the bilinear interpolant: if
its sign matches the diagonal corners they are joined, otherwise separated.
In three dimensions the same ambiguity leaves holes in the surface, which is
why the decider exists at all.
