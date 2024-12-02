# Convex hulls

The smallest convex set containing a point set, used everywhere as a cheap
conservative stand-in for a complicated shape. Being convex is what makes it
cheap: a point is inside exactly when it is on the inner side of every edge,
with no special cases.

Three algorithms, differing in what they sort.

| algorithm | cost | sorts by |
|---|---|---|
| Andrew's monotone chain | `O(n log n)` | x coordinate |
| Graham scan | `O(n log n)` | angle around a pivot |
| gift wrapping (Jarvis) | `O(n h)` | nothing |

Monotone chain is the one to reach for. It is simpler than Graham's scan and
better behaved numerically, because sorting by coordinate needs no arctangent
and no division, only the same turn predicate the rest of the algorithm uses.

Gift wrapping is the only output-sensitive one: its cost depends on how many
hull points there are, so it wins when a million points have a hull of five and
degrades to `O(n^2)` when they are all on a circle.

## Verified

- the three agree on **2000** random sets including duplicates and collinear
  runs: 0 disagreements
- against a brute-force `O(n^3)` check on 400 sets: 0 hull vertices that the
  brute force did not also find
- 1000 hulls are all convex, and 0 input points lie outside their own hull
- rotating callipers matches brute-force farthest pair over 500 sets exactly,
  difference 0.00e+00

## What the hull looks like on random data

Uniform points in a disc:

| points | hull vertices | hull area (disc is 3.1416) |
|---|---|---|
| 10 | 6 | 1.02 |
| 100 | 16 | 2.70 |
| 1000 | 34 | 3.03 |
| 10000 | 75 | 3.12 |

The hull grows roughly as the cube root of the sample size, which is why
output-sensitive algorithms are worth having.

## Related

The naive `O(n^3)` hull, one candidate edge per pair of points, is in
[dap2-practice/convex-hull](../../../dap2-practice/convex-hull/) as a Java
program from the algorithms course. It is the same problem approached from the
complexity side rather than the modelling side.
