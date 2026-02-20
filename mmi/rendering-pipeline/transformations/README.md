# Transformations

Homogeneous coordinates: a fourth coordinate `w` turns translation into a
linear operation, so the entire model-view-projection chain collapses into one
4x4 matrix per vertex.

The convention is column vectors with the matrix on the left, so a chain reads
right to left: `translate(10,0,0) @ rotate_z(90°)` applied to `(1,0,0)` gives
`(10,1,0)`, and the same two in the other order give `(0,11,0)`.

## What `w` is actually for

Setting `w = 1` marks a point and `w = 0` marks a direction, and the same
matrix then does the right thing for both: translating `(1,0,0)` as a point
gives `(6,5,5)` under `translate(5,5,5)`, and as a direction gives `(1,0,0)`
unchanged. A direction has no position, so translating it is meaningless, and
the fourth coordinate is what encodes that difference rather than a separate
code path.

## Why normals need their own matrix

Under a non-uniform scale a normal transformed like a direction stops being
perpendicular to its surface. With `scale(3,1,1)`, a normal and its tangent
start perpendicular; after the naive transform their dot product is **-4.0**
instead of 0, and every lighting computation on that surface is wrong. The
inverse transpose keeps it at 0 to machine precision, which is why
`normal_matrix` exists as a separate thing to upload to the shader.

## Verified

- `rotate_axis` reproduces `rotate_x`, `rotate_y` and `rotate_z` to 1.11e-16
  over 200 random angles each
- `inverse` round-trips 300 random chains of translate, rotate, scale and shear
  to 8.88e-15
- `look_at` preserves distances over 200 random cameras to 3.55e-15, which is
  the definition of a rigid motion, and puts the eye exactly at the origin with
  the target on the negative z axis
- `rotate_about` leaves its pivot fixed exactly
