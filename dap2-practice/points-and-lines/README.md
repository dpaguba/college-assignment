# Points and lines

Point, line, and the side test. Practical sheet 4, task 4.1.

```
java Application 5 678
Vergleiche Punkte mit der Geraden (69.35, 11.01) -- (2.17, 54.35)
Punkt (34.56, 60.49) liegt rechts der Linie.
Punkt (20.47, 18.48) liegt links der Linie.
Punkt (30.84, 19.94) liegt links der Linie.
```

Or with explicit coordinates: `java Application 1 1 3 3 2 2 1.5 3 0 0 0 1.0`.

## The one primitive

`Line.side(p)` is the sign of the cross product of (end − start) and
(p − start). Geometrically that is twice the signed area of the triangle, so it
is zero exactly when the three points are collinear and its sign says which way
the triangle is wound.

That single predicate is the whole of the convex hull in the next task, and of
most planar geometry besides. No division, no square root, no trigonometry, and
on integer input it is exact. Computing the line's slope and comparing y values
would need a special case for vertical lines and would lose exactness; this
does neither.

## isBetween

Only called on three collinear points, which is what makes it cheap: comparing
coordinate ranges is enough, no projection needed. Both coordinates have to be
checked, because a vertical segment has constant x and a horizontal one
constant y.

## Locale

Every coordinate is formatted with `Locale.ROOT`. On a German system the default
locale prints 13.12 as "13,12", which would break every line of the expected
output and every comma-separated list along with it.

## Verification

Both sample calls, including the exact generated coordinates for seed 678,
which pins down the generator: x before y, points in order, `nextDouble() *
(max − min) + min`. All six error cases match too.
