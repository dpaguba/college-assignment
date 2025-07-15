# Convexity

A set is convex when it contains the segment between any two of its points,
and that property is what makes an optimisation problem tractable: on a
convex region with a convex objective, a local optimum is global.

The tenth sheet's four sets:

| set | convex |
|---|---|
| Ax ≤ b, x ≥ 0 | yes |
| the same with x in {0,1} | no |
| a disc | yes |
| adding a linear constraint to a convex set | stays convex |

The second row is the whole reason integer programming is a separate subject.
The feasible points of a linear program form a convex polyhedron; the integer
points inside it do not, so nothing about following an improving direction
carries over.

The module checks convexity by sampling segments rather than by citing the
definition, which is a test of the reasoning on an example rather than a
proof.
