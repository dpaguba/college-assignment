# What the equivalence on slide 25 needs

The slide sets the decomposition of the term-document matrix next to the
eigen-analysis of `Σ fᵢ fᵢᵀ`, and next to that the covariance matrix. The
first pairing is an identity; the second holds only under a condition the
slide does not state.

## The part that always holds

From `F = U S Vᵀ` follows `Fᵀ F = V S² Vᵀ`, which is an eigen-decomposition.
So the squared singular values are the eigenvalues of the scatter matrix and
the right singular vectors are its eigenvectors. Checked numerically, and the
scatter matrix checked against the literal sum of outer products.

## The part that needs centring

The scatter matrix equals the covariance matrix only after the mean is
subtracted. Term vectors are never mean-free: every entry is a frequency and
therefore not negative. So the strongest direction of the uncentred scatter
matrix points roughly at the mean, and the mean says nothing about the
differences between documents.

Measured on a random non-negative matrix:

| | angle to the mean |
|---|---:|
| without centring | small |
| after centring | large |

and the first axis agrees with the one from principal component analysis only
in the second case. The module reports both angles and both verdicts.

## Why it matters in practice

Skipping the centring step wastes the first component on a direction everyone
already knows. On a term-document matrix that is not a small effect, because
the mean vector is large compared with the variation around it.
