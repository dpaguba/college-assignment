# Convex hull

Andrew's monotone chain: sort the points, sweep once for the lower chain and
once for the upper, discarding any point that fails to turn left.

On the ten points of the third exercise sheet the hull is
A(0,0), J(1,0), I(2,1), H(2,2), G(1,4), F(0,4). The points B(0,1), C(1,1),
D(1,2) and E(0,3) are not vertices; B and E lie on the left edge, C and D
lie inside.

## Checked against the definition

A point is a hull vertex exactly when some direction makes it the unique
furthest point. The check scans 3600 directions and collects the unique
maximisers, using neither sorting nor cross products, and returns the same
set of vertices. It also handles the two cases that trip up an
implementation: a point strictly inside, and a point on an edge but not a
vertex.

Three collinear points give two hull vertices, not three, which is the
convention this implementation follows.
