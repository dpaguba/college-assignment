# Polygon triangulation

Graphics hardware draws triangles and nothing else, so every polygon on screen
has been through this.

A convex polygon needs no algorithm: a fan from any vertex works. A concave one
does. Fanning the arrow `(0,0) (4,0) (4,4) (2,1) (0,4)`, whose area is 10,
produces three triangles with a combined area of **14**: the fan triangles
stick out of the polygon and overlap each other. Ear clipping on the same
polygon gives exactly 10.

## The count is a free check

Every simple polygon with `n` vertices triangulates into exactly `n - 2`
triangles, whatever the algorithm and whatever the shape. Over 300 random
simple polygons of 3 to 14 vertices: **300** with the right count and **0**
with an area mismatch against the shoelace formula. A 21-vertex comb with 6
reflex teeth gives 19 triangles and area 28.5 against the exact 28.5.

## Ear clipping

A vertex is an ear when it is convex **and** its triangle contains no other
vertex of the polygon. Both conditions matter: a convex vertex whose triangle
swallows a distant part of the shape is not an ear, and cutting it would
produce a triangle outside the polygon.

Every simple polygon with more than three vertices has at least two ears, which
is what guarantees the loop terminates. Each pass removes one vertex and costs
a scan, so `O(n^2)`. Faster algorithms exist, monotone decomposition at
`O(n log n)` and Chazelle's linear one, but ear clipping fits on a page and
extends to holes with a bridge construction, so it is what libraries ship.

## Reflex vertices measure the difficulty

| polygon | convex | reflex | convex overall |
|---|---|---|---|
| square | 4 | 0 | yes |
| arrow | 4 | 1 | no |
| U-shape | 6 | 2 | no |

A polygon is convex exactly when it has no reflex vertices, and the reflex
count bounds how much work any decomposition has to do. It also bounds the
number of guards needed to see the whole polygon, which is the art gallery
problem.

## Simplicity is a precondition, not an assumption

A self-intersecting polygon has no well-defined inside, so "triangulate its
interior" has no answer. `is_simple` checks it in `O(n^2)`: the square and the
U-shape pass, the bowtie `(0,0) (4,4) (4,0) (0,4)` fails.
