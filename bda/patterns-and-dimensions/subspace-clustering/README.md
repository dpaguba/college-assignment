# Subspace clustering

In high dimensional data a group can be tight in three attributes and spread
out in the other forty, so it is invisible in the full space and obvious in
the subspace. The module builds such a case: four points forming a cluster in
two dimensions and noise in the other three, found in the projection and not
in the full space.

Searching for it means searching the subspaces, and there are 2ⁿ − 1 of them:
1023 for ten dimensions.

The pruning rule is the Apriori rule again. A set of points dense in a
subspace is dense in every projection of it, so a subspace whose projection
is not dense can be skipped. Density is anti-monotone in the dimensions
exactly as support is anti-monotone in the items, and the same level-wise
search applies.
