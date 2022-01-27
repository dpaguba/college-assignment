# Convex hull

The smallest convex polygon containing every point.

| | |
|---|---|
| Time | O(n log n), dominated by the sort |
| Recurrence | `not recursive here` |
| Master theorem | not applicable |

## The idea

Two methods, both O(n log n), both built from a single primitive: the cross product,
which says whether three points turn left, right, or lie in a line. Every convex
hull algorithm is that one test in a loop.

**Andrew's monotone chain** sorts by coordinate and sweeps twice, once for the lower
boundary and once for the upper, popping any point that would turn the wrong way.

**Graham's scan**, the 1972 original, sorts by the angle each point makes with the
lowest one, then walks the list keeping only left turns.

## What is worth noticing

The comparison between them is the lesson. Sorting by angle needs `atan2`, so the
comparison is floating point and points at equal angles have to be ordered by
distance as a tiebreak. The monotone chain sorts by coordinate and uses only
multiplication and subtraction, so on integer input it is exact.

Same complexity, and one of them cannot produce a wrong answer from rounding. Both
are here so the difference is visible rather than asserted.
