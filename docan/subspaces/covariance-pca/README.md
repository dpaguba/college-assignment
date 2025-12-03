# Covariance and principal axes

The mean is the origin of the new coordinate system, the eigenvectors of the
covariance matrix are its axes, and the eigenvalues are the variances along
them. Because the matrix is symmetric, the eigenvalues are real and the
eigenvectors orthogonal, which is what makes a coordinate system out of them
at all.

Divided by N rather than N−1, so that the eigenvalues are exactly the
variances of the transformed data. The module checks that: after the rotation,
the variance along axis j equals eigenvalue j, and the off-diagonal entries of
the covariance are zero.

## What the rotation does not change

The sum of the variances, and the distances between the points. The rotation
only redistributes the spread across the axes; it creates and destroys
nothing. Everything the method costs is paid in the next step, when axes are
dropped.

## The check that matters

Transforming and transforming back returns the original points exactly. A
rotation that does not is not a rotation, and the test catches a sign or
transpose error that reads as correct on the page.
