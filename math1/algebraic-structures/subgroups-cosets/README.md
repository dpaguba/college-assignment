# Subgroups and cosets

Lagrange's theorem is a counting argument: the cosets of a subgroup partition
the group and all have the size of the subgroup, so the order of a subgroup
divides the order of the group. Both halves are checked here over every
subgroup of every group in the sample.

| group | order | subgroups | normal |
|---|---:|---:|---:|
| Z12 | 12 | 6 | 6 |
| S3 | 6 | 6 | 3 |
| D4 | 8 | 10 | 6 |
| Q8 | 8 | 6 | 6 |
| Z2 × Z2 | 4 | 5 | 5 |

The cyclic group of order 12 has exactly one subgroup per divisor of 12,
which is the converse of Lagrange holding for cyclic groups and failing in
general.

## The row that is worth stopping at

Q8 is not abelian and every one of its six subgroups is normal. That
combination is unusual enough to have a name, and it kills the natural guess
that normality is a way of saying "the group is nearly abelian". The
symmetric group on three points is the contrast: of its six subgroups, three
are normal and three are not, and the three that are not are exactly the
subgroups of order two.

Those are the subgroups for which left and right cosets differ, which is what
the next module needs.
