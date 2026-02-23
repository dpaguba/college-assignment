# Visibility

Deciding what is in front of what. Three answers that differ in where the
sorting happens: per polygon, per pixel, or once at build time.

## The z-buffer

One depth per pixel, keep whichever fragment is nearer. All six submission
orders of three overlapping surfaces produce **one** identical image, which is
the property that matters: no sorting, no preprocessing, no restrictions on the
geometry.

Order still affects the work done. Front to back, 4096 of 12288 fragments
survive the depth test, an overdraw of 33%. Back to front, all 12288 win and
are then overwritten, an overdraw of 100%. This is why engines sort roughly
even though they do not have to sort at all.

The price is memory, which is why it took until the nineties to become
standard, and transparency, which it cannot do: a fragment behind a transparent
one is discarded before anything can blend it.

## Why the painter's algorithm cannot be fixed

Sorting polygons by centroid distance fails whenever their depth ranges
overlap, and three long triangles can be arranged so that each occludes the
next in a cycle, where **no** ordering of the three is correct.

Measured on three mutually intersecting triangles over 400 random cameras at
60x60 pixels, against a depth-tested reference:

| method | cameras with a wrong pixel | worst case |
|---|---|---|
| painter's, sorted by centroid | 400 of 400 | 1341 pixels |
| BSP traversal order | 0 of 400 | 0 pixels |

## The BSP tree

Sort once, at build time, and the tree yields an exact back-to-front order for
any camera in linear time. Stand at the camera, ask which side of the node's
plane it is on, render the far subtree, the node, then the near one; nothing in
the far subtree can occlude anything in the near one because the plane
separates them. This is what Doom did.

The cost is polygon count. The three intersecting triangles above become 6
polygons in the tree, and `n` mutually intersecting planes grow to about `2n`.
Choosing good splitting planes is the entire engineering problem.

`plane_of` uses Newell's method rather than the cross product of the first two
edges, and the difference is not cosmetic: a split inserts a vertex on an
existing edge, so the first three vertices of a split piece are frequently
collinear and the cross product is zero.

## The bug this found

The BSP order disagreed with the reference on every camera until the cause
turned out to be elsewhere: `rasterise_triangle` was returning barycentric
weights in its internal vertex order rather than the caller's, so the
interpolated depth of every clockwise piece belonged to the wrong vertex. See
[rasterisation](../rasterisation/). Nothing in reading the visibility code
would have shown it.
