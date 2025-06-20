# Delaunay and Voronoi

A triangle belongs to the Delaunay triangulation when its circumcircle
contains no other point. The implementation tests every triple, which costs
the fourth power of the point count and is meant for looking at rather than
for running on the fifty points the exercise generates in R.

Three properties are checked on random point sets: every circumcircle is
empty, the triangles together cover exactly the convex hull (areas agree to
1e-9), and no triangle overlaps another.

## Maximising the smallest angle

Of the two ways to split a quadrilateral into triangles, the Delaunay choice
is the one whose smallest angle is larger. On the quadrilateral in
`angle_comparison` it is 18.4° against 4.4°: the other diagonal produces a
sliver. This is the property that makes the triangulation useful for
interpolation, where thin triangles are where the error lives.

## The duality

Two points share a Delaunay edge exactly when their Voronoi cells share a
border. The module samples the plane on an 80 × 80 grid, assigns each sample
to its nearest centre, reads off which cells touch, and checks that every
Delaunay edge appears there. The Voronoi vertices are the circumcentres of
the Delaunay triangles.

## Four points on a circle

The unit square has all four corners on one circle, so both diagonals give
empty circumcircles and the triangulation is not unique. The module reports
that rather than picking one silently.
