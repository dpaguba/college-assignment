# Linear maps

A linear map is determined by what it does to a basis, so a matrix is a map
written down with respect to two bases. Change either basis and the matrix
changes while the map does not.

The columns of the matrix are the images of the source basis, expressed in
the target basis. With standard bases those coordinates are the components,
which is why the distinction is easy to miss until a basis changes: the same
shear has matrix `[[1,1],[0,1]]` in the standard basis and a different one in
the basis `(1,1), (1,-1)`.

## What survives a change of basis

Composition of maps is multiplication of matrices, verified here by applying
both sides to several vectors rather than by comparing the matrices, so the
claim is about the maps.

The quantities that describe the map itself are the ones invariant under
conjugation: the rank, the determinant, the eigenvalues. The determinant of a
matrix and of the same map in another basis agree, which the tests check, and
that invariance is what lets the next modules speak of the determinant of a
map at all.
