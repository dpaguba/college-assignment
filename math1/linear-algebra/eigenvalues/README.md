# Eigenvalues

A direction the map only stretches, and the factor by which it stretches it.

The characteristic polynomial is built here in exact arithmetic by evaluating
det(A - xI) at enough points and interpolating, so its coefficients are the
trace and the determinant exactly. For a two by two matrix the polynomial is

```
x^2 - trace(A) x + det(A)
```

and the tests check both coefficients against the separately computed trace
and determinant.

## Two different failures

**A rotation has no real eigenvalue.** Every direction is turned, so nothing
is merely stretched, and the characteristic polynomial has no real root. The
module reports an empty list.

**A shear has an eigenvalue and too few eigenvectors.** The matrix
`[[1,1],[0,1]]` has 1 as its only eigenvalue and a one-dimensional
eigenspace, so it cannot be diagonalised even though its eigenvalue is
perfectly real. Diagonalisability is a statement about eigenvectors spanning
the space, and the tests separate it from the existence of eigenvalues.

The search for roots covers the rationals only, by the rational root theorem,
so the scope is exactly stated: complete for rational eigenvalues, silent
about the rest. Checked against numpy on 100 random matrices, where every
rational eigenvalue found also appears in the numerical spectrum.
