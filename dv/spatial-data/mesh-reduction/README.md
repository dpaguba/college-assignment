# Mesh reduction

Contract an edge onto its midpoint: one vertex disappears and the triangles
containing both endpoints collapse away. Which edge to take is decided by the
quadric error metric, the sum of squared distances to the planes of the
triangles meeting at the two endpoints.

The example mesh is a triangulated paraboloid rather than a flat grid.
On a flat mesh every plane is the same plane, every error is zero, and the
metric says nothing; on the curved one the cheapest edge costs 0.018 and the
most expensive 0.196, so the choice has content.

Measured as the largest distance from an original vertex to the nearest
remaining triangle plane, the error after four contractions is twice that
after two. Reduction is not free, and the metric is what keeps the cost
where the surface is flattest.
