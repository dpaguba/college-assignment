# Alpha shapes

With the lecture's negative parameter, an α-ball is the complement of a disc
of radius 1/|α|. Two points are joined in the α-shape when a disc of that
radius passes through both and contains no other point.

For α = −0.5 the radius is 2. Every edge produced by the implementation was
checked directly against that definition on 25 random point sets and two
radii: an edge is present exactly when an empty certifying disc exists.

## What α = −0.5 gives on the exercise points

The same boundary as the convex hull, with the two collinear points B(0,1)
and E(0,3) inserted on the left edge, eight edges forming one closed cycle.
No indentation of this point set is deep enough for a disc of radius 2 to
reach into it. The shape first differs from the hull at α = −1, radius 1,
where the interior points C(1,1) and D(1,2) start to be reached.

That is also the answer to what separates the α-hull from the α-shape. Both
have the same vertices; the hull's boundary is made of circular arcs of
radius 2 bulging inwards between consecutive points, and the shape replaces
each arc by the straight segment between its ends.

## Below the smallest distance

The nearest two points are 1 apart, so a radius below 0.5 can no longer pass
through any pair and the shape falls apart into isolated points, with no
edges at all. The module measures that threshold rather than assuming it.
