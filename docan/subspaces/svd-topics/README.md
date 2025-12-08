# The topic space

The singular value decomposition of the term-document matrix gives the same
structure as principal component analysis without the detour through the
covariance matrix: the left singular vectors span the subspace, the singular
values scale the axes, and the right singular vectors are the coordinates of
the documents.

## The best approximation of rank k

By the Eckart-Young theorem the Frobenius error of the rank-k truncation is
exactly the root of the sum of the discarded squared singular values, and no
other matrix of rank k comes closer. Both halves are checked: the identity
numerically over 30 random matrices, and the optimality by perturbing the
optimal factorisation 400 times in each of many directions and never finding
anything better.

Testing against arbitrary random rank-k matrices would prove nothing, since
they are far off anyway. Perturbing the optimum is the version of the test
that could actually fail.

## What the subspace buys

Terms that occur together are folded onto one axis, so two documents about the
same subject with different vocabulary become similar. That is exactly the gap
a comparison of raw term vectors leaves open.

## What it does not buy

The axes carry no meaning. They are sorted by variance, not by
interpretability, and a single axis routinely mixes words with nothing in
common. Anyone naming a topic after the largest entries of an axis is reading
something into it that the method did not put there.
