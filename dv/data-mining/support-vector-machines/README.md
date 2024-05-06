# Support vector machines

The separating hyperplane with the widest margin. The dual problem is solved
by pairwise coordinate ascent, which keeps the constraint Σ αᵢyᵢ = 0 intact
by moving two multipliers at once.

## The margin, checked independently

The margin from the dual is compared with a direct search: for 7200
directions, project both classes and take half the gap. On the exercise-style
data both give 1.11803, and over 25 random separable problems the two agree
to within 0.0004. The direction search uses no dual, no gradient and no
kernel, so agreement is evidence rather than a tautology.

## Only the boundary matters

Two of the four points carry a non-zero multiplier and the other two carry
none. Adding a point 50 units away on the correct side changes the normal
direction by exactly zero. That is the meaning of the name: the solution is
supported by the points at the margin and by nothing else.

## Kernels and slack

The four points of exclusive-or cannot be separated by a line: their convex
hulls meet, at distance 0, which the module computes with a Frank-Wolfe
iteration on the difference set. Mapped to the quadratic features
(x, y, x², y², xy) the hulls come apart and a hyperplane exists. That is what
a kernel buys, without ever building those coordinates.

Slack variables buy the other case, data that is not separable in any space
one is willing to use: a point may sit inside the margin or on the wrong
side, at a price. A large penalty gives a narrow margin with few violations,
a small one a wide margin with more. Without slack the fit on contradictory
data raises rather than returning a plane that is not there.
