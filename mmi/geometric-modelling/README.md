# Geometric modelling

How a shape is represented before anything draws it.

| Topic | Representation |
|---|---|
| [bezier-curves](bezier-curves/) | a curve from a control polygon |
| [b-splines](b-splines/) | the same, with fixed degree and local control |
| [mesh-structures](mesh-structures/) | a surface as vertices, edges and faces |
| [marching-squares](marching-squares/) | a shape as the level set of a field |
| [convex-hull](convex-hull/) | the cheap conservative bound on a point set |
| [polygon-triangulation](polygon-triangulation/) | a polygon as triangles, which is all hardware draws |
| [delaunay-voronoi](delaunay-voronoi/) | a point set as a well-shaped triangulation, and its dual |

## The thread running through all of them

Each representation is chosen for what it makes easy. Control polygons make
editing easy and evaluation slightly awkward. Meshes make rendering easy and
smoothness awkward. Level sets make topology changes easy, which is why fluid
and metaball systems use them, and exact boundaries awkward.

The convex hull property appears three times: it bounds a Bezier curve, it
makes subdivision-based flattening valid, and it is the reason a point-inside
test on a hull is a loop of sign tests with no special cases.

## Verification note

Four bugs in this block were invisible on reading and only appeared under
measurement: a flatness test measured to a line instead of a segment, a
marching-squares case table written for a different edge numbering, a
plane-fitting cross product on collinear vertices, and a Delaunay super
triangle twenty times too small. Each produced output that looked plausible,
and three of them passed the obvious correctness test for their own module.
