# Delaunay triangulation and Voronoi diagrams

Many triangulations of a point set exist and they are not equally good. Long
thin triangles interpolate badly, shade badly and make solvers
ill-conditioned. The Delaunay triangulation maximises the smallest angle over
all triangulations of the same points, and its defining property is local and
checkable: no point lies inside the circumcircle of any triangle.

The Voronoi diagram is the same information read the other way, and the duality
is one line: a Voronoi vertex is the circumcentre of a Delaunay triangle.

## Verified

Over 300 random point sets of 4 to 40 points:

- 0 violations of the empty-circumcircle condition
- 0 disagreements with the triangle count `2n - 2 - h`
- the triangles cover exactly the convex hull, worst relative area error
  **1.04e-15**

At 1000 points the count is still exact (1979 triangles) and the area error is
1.8e-15, and it holds across coordinate scales from 1e-3 to 1e6.

Over 2000 random convex quadrilaterals the Delaunay triangulation equals the
better of the two possible triangulations **2000** times and is worse **0**
times. On a 12-point zigzag it achieves a smallest angle of 21.80° where the
fan triangulation of the same points manages 2.08°.

## The two bugs, and why neither was visible

**The empty-circumcircle test does not catch missing triangles.** The first
version produced triangulations with holes on 33 of 300 point sets, and every
one of them passed `is_delaunay`, because a hole violates nothing. Only the
triangle count and the covered area found it.

**The super triangle has to be enormous.** "Large enough to contain the points"
is the natural requirement and it is wrong. Hull triangles have a super-triangle
vertex as their third corner, so their circumcircles depend on where it is, and
unless it is effectively at infinity the algorithm deletes the wrong triangles
near the hull:

| super triangle, in bounding boxes | broken sets of 300 |
|---|---|
| 2 | 181 |
| 20 | 33 |
| 100 | 10 |
| 1000 | 1 |
| 100000 | **0** |

The predicate was also rewritten from a distance-against-radius comparison to
the sign of a determinant in coordinates relative to the query point, which
avoids constructing the circumcentre at all. The centre of a nearly degenerate
triangle is enormous and far away, and subtracting two such distances cancels
nearly every significant digit.

## The degeneracy that remains

Eight points placed exactly on one circle produce 9 overlapping triangles
covering 532.8 units of a hull whose area is 282.8. The determinants that
should be exactly zero evaluate to -9.1e-13 and -1.5e-11 instead, so the
algorithm makes contradictory decisions.

Displacing the points by 1e-12 fixes it, 20 times out of 20; at 1e-15 it works
3 times out of 20 and at 0 never. That is the cheap version of what production
code does deliberately, under the name simulation of simplicity, and the real
answer is exact arithmetic for the predicate.

## The duality, checked against a raster

Rasterising `nearest_site` over a 400 x 400 grid and collecting which cells
touch gives 24 adjacent pairs. The Delaunay edges number 27. Every raster pair
is a Delaunay edge; the three Delaunay edges with no visible shared boundary
are hull edges, whose dual Voronoi edges are rays running out of the sampled
box, plus one whose shared boundary is shorter than the raster step.

Each Voronoi vertex is equidistant from exactly three sites to 2.13e-13, and no
fourth site is nearer.
