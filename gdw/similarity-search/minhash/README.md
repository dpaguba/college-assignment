# MinHash

Take a random permutation of the universe and record the smallest element of
each set under it. The two minima agree exactly when the smallest element of
the union lies in the intersection, which happens with probability equal to
the Jaccard similarity.

A set of ten thousand elements becomes a signature of a hundred numbers, and
the comparison becomes a hundred integer equalities.

## The permutation has to be a good one

The first implementation here used the standard linear family, a multiplier
and an offset modulo a prime. That family is pairwise independent and the
minimum under it is not uniformly distributed over the union, and the
estimates were consistently wrong:

| true similarity | estimated |
|---|---|
| 0.667 | 0.691 |
| 0.333 | 0.306 |

A bias of about 0.025 in both directions, far outside the sampling error of
0.007 over eight seeds. Replacing the linear family with a proper avalanche
mixer brings the error under 0.009, which is what the sampling error predicts.

That is the kind of defect an estimator hides well: the numbers looked
plausible, the tests with a loose tolerance passed, and only averaging over
several seeds made the systematic part visible.
