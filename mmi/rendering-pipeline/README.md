# The rendering pipeline

A vertex enters as three numbers in some object's own coordinates and leaves as
a colour in a pixel. These are the stages in between, in order.

| Stage | Topic |
|---|---|
| place the object and the camera | [transformations](transformations/) |
| flatten to an image plane | [projection](projection/) |
| discard what is outside | [clipping](clipping/) |
| find the covered pixels | [rasterisation](rasterisation/) |
| decide what is in front | [visibility](visibility/) |
| compute the brightness | [lighting](lighting/) |

[ray-tracing](ray-tracing/) is the alternative to the whole chain: the same
image from the transposed loop, one ray per pixel instead of one pass per
triangle.

## What the stages have in common

Each stage exists because the previous one made an assumption the next cannot
hold to. Projection makes distant things small, so interpolation across a
triangle stops being linear and the rasteriser needs `1/w`. The perspective
divide breaks down behind the camera, so the clipper has to run before it. The
rasteriser produces fragments in arbitrary order, so visibility has to be
resolved per pixel rather than per triangle.

## Verification note

Two bugs here were invisible on reading and only appeared when the modules were
run against each other: barycentric weights returned in the wrong vertex order
for clockwise triangles, and a plane computed from three collinear vertices of
a freshly split polygon. Both surfaced as "the BSP order is wrong", and neither
was in the visibility code.
