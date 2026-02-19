# Ray tracing

Rasterisation asks, for each triangle, which pixels it covers. Ray tracing asks
the transposed question: for each pixel, which surface is there. The loops swap
places, and everything follows from that.

Because a ray can start anywhere and point anywhere, shadows, reflection and
refraction are all the same operation applied again from a new origin. In a
rasteriser each of those is a separate mechanism with its own approximation.

## The intersections

**Sphere**: substitute the ray into the sphere equation, solve the quadratic,
take the smaller positive root. Hit points land on the sphere to 9.77e-15 over
3000 random rays.

**Triangle**, by Moller-Trumbore: solve for the ray parameter and both
barycentric coordinates at once by Cramer's rule, without ever constructing the
plane. Over 5000 random rays it agrees with an independent plane-plus-inside
test on every case, 0 missed hits, and the point rebuilt from the barycentric
coordinates matches the point on the ray to 9.99e-16.

**Box**, by the slab method: three intervals of `t`, one per axis, intersected.
Against an independent implementation that tests all six faces separately,
**0 disagreements in 200000 random rays**, including rays starting inside the
box and rays exactly parallel to an axis. This is the test a bounding volume
hierarchy runs millions of times per frame and never draws anything with.

## Refraction

Snell's law reproduces the textbook angles: 30 degrees into glass refracts to
19.47, 60 degrees to 35.26. Going the other way, out of glass, the critical
angle at 41.8 degrees appears on its own: 41 degrees still refracts, at 79.77
degrees, and 42 degrees returns `None`, total internal reflection. A ray tracer
gets that effect from the arithmetic rather than from a special case.

Schlick's approximation gives 4% reflectance head on and 92% at 89 degrees,
which is why glass seen face on is transparent and seen edge on is a mirror.

## Shadows and the offset

A shadow ray is exact, because the question is asked rather than approximated.
Adding a 1.1-radius blocker to a scene with one sphere darkens **571** pixels
of a 61x61 image, and every one of them drops to exactly 0.0400, which is the
ambient term and nothing else.

The offset along the normal is not optional. Take a hit point carrying 3e-9 of
accumulated error inward, the amount a few bounces produce, and the surface
reports itself as blocking its own light. Offsetting the shadow ray's origin by
1e-8 fixes it. Without that, the image is covered in the speckle known as
shadow acne.

## Recursion depth

A mirror sphere next to a bright one, brightest point on the mirror:

| depth | brightness |
|---|---|
| 1 | 0.0478 |
| 2 | 0.6580 |
| 3 | 0.6580 |
| 4 | 0.6580 |

Depth 1 is no reflection at all. Depth 2 shows the neighbour. Beyond that
nothing changes here because the neighbour is not itself reflective, which is
the general pattern: two bounces are usually indistinguishable from ten, so the
recursion is capped rather than run to convergence.
