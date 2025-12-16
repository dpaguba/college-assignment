# Subspaces

| Module | Topic |
|---|---|
| [covariance-pca](covariance-pca/) | the covariance matrix and its axes |
| [dimensionality-reduction](dimensionality-reduction/) | the price of dropping axes |
| [svd-topics](svd-topics/) | the topic space and the best rank-k matrix |
| [pca-svd-equivalence](pca-svd-equivalence/) | what slide 25 needs and does not say |

Everything here is exact and can therefore be checked exactly. The
reconstruction error equals the sum of the discarded eigenvalues, the
Frobenius error of the truncation equals the root of the discarded squared
singular values, and the squared singular values equal the eigenvalues of the
scatter matrix. All three are verified numerically rather than quoted.

The fourth module is the one with something to say: the equivalence the slide
draws between the scatter matrix and the covariance matrix holds only after
the mean is subtracted, and term vectors are never mean-free.
