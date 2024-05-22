# Principal axes

The first exercise asks for the transformation by hand, through the roots of
the characteristic polynomial, on the four points (0,1), (1,1), (2,1), (3,2).

Mean (1.5, 1.25). Covariance with the divisor n − 1:

|  | x | y |
|---|---|---|
| x | 5/3 | 1/2 |
| y | 1/2 | 1/4 |

Characteristic polynomial λ² − (23/12)λ + 1/6, roots 1.8254 and 0.0913.

The first axis carries 1.8254 / 1.9167 = **95.24 %** of the variance. Dropping
the second axis therefore loses under five percent, which is the answer to
what the result says about a possible reduction.

## Checked against numpy

The covariance matches `numpy.cov`, the eigenvalues match `numpy.linalg.eigvalsh`
to 1e-14 over 200 random matrices, and each eigenvector satisfies Av = λv to
the same accuracy. The transformed points match a projection built from
`numpy.linalg.svd`, up to the sign of an axis, which is free.

The total variance is the same before and after the transformation. That is
what the rotation does: it moves the variance between the coordinates without
creating or destroying any.
