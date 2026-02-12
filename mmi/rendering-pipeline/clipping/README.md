# Clipping

Not an optimisation. Geometry behind the camera has a negative `w`, and after
the perspective divide it comes back in front of the camera, mirrored. A
triangle straddling the camera renders as a shape that exists nowhere in the
scene, so the near plane clip is mandatory.

## Three algorithms, three ideas

**Cohen-Sutherland** encodes each endpoint as four bits saying which sides of
the window it is beyond. Both codes zero accepts immediately, a non-zero
bitwise and rejects immediately, and the remaining cases are cut one edge at a
time. Two integer operations decide the common cases, which is the whole point.

**Liang-Barsky** treats the segment as `p + t d` and narrows the interval of
`t` directly. No iteration, and it hands back the parameter values, which is
what an interpolating rasteriser needs for the attributes at the new endpoints.

**Sutherland-Hodgman** clips a polygon against one window edge at a time, four
passes for a rectangle. Its known flaw is that the output is always a single
closed polygon: a concave shape that leaves and re-enters comes back as two
pieces joined by a degenerate edge along the boundary. Convex input never
triggers it.

## Verified

- the two line clippers agree on **20000** random segments to 1e-9, with 0
  disagreements about whether the segment is visible at all
- Liang-Barsky's clipped endpoints match a dense parameter sweep along the
  original segment on 2000 random cases, 0 disagreements
- the polygon clipper's output area matches a Monte Carlo estimate of the
  intersection: 100.000 against 100.000 for a square, 25.000 against 25.038 for
  a triangle, 95.321 against 95.310 for a skewed quadrilateral
- `clip_near_plane` puts every new vertex exactly on the plane, and turns the
  two-vertices-inside case into two triangles, which is why a renderer can emit
  more triangles than it was given

## Back-face culling

One sign test on the screen-space area. Half the triangles of a closed opaque
mesh face away at any moment and none of them can be visible, so this halves
the work before a single pixel is touched.
