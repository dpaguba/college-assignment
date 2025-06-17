# Transformations

Homogeneous coordinates exist so that a translation can be a matrix. Without
the third row a translation is an addition and cannot be composed with
rotation and scaling in one product.

Composition is checked against numpy's matrix product, and applying a matrix
to a point against numpy's own multiplication followed by the perspective
divide.

## Order matters

Rotating and then translating is not the same as translating and then
rotating; the module measures the two results and they differ. This is the
most common source of a transformation that looks nearly right.

A full turn returns exactly to the starting point, and the inverse of a
rotation is the rotation by the opposite angle.

## Affine or not

The last row tells them apart. `(0, 0, 1)` means affine: parallel lines stay
parallel. A perspective matrix puts a value in the last row, the divide by
the depth follows, and the far point moves towards the centre. That divide is
what makes a projection a projection.
