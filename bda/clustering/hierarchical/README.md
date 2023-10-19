# Hierarchical clustering

Merge the closest pair, repeat, keep the record. The result is a tree that
can be cut at any height, so the number of clusters is chosen after seeing
the structure rather than before.

The distance between clusters is where the choice moved:

| linkage | takes | behaviour |
|---|---|---|
| single | the closest pair of members | chains |
| complete | the furthest pair | compact, splits elongated groups |
| average | the mean over all pairs | between the two |

On six points in a line one step apart, single linkage puts all of them in
one cluster because every neighbour is close, and complete linkage splits the
line because its ends are far apart. Same data, two answers, and the linkage
is the entire reason.
