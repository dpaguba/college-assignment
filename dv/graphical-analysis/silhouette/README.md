# Silhouette coefficient

For each point: `a` is the mean distance to its own group, `b` the mean
distance to the nearest other group, and the value is (b − a) / max(a, b). It
sits between −1 and 1, and a negative value means the point would be happier
elsewhere.

The implementation is checked against the definition recomputed from scratch
on 60 random labellings.

A clean split of two well-separated pairs scores above 0.9; deliberately
splitting each pair across both groups scores below zero. On six points in
two obvious clumps, the coefficient picks k = 2, which is what it is for: it
compares different numbers of groups, where the k-means objective cannot.

The usual reading: above 0.7 strong structure, 0.5 to 0.7 reasonable, 0.25 to
0.5 weak, below that none worth speaking of.
