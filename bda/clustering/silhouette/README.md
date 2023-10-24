# The silhouette coefficient

For each point, compare the average distance to its own cluster with the
average distance to the nearest other one. Near one the point is well placed,
near zero it sits on a boundary, and below zero it is closer to another
cluster than to its own.

That last case is what makes the measure useful. On four points in two
obvious pairs, the correct clustering scores above 0.9 and the crossed one
scores below zero, so a wrong answer is not merely worse, it is negative.

Averaging over the points gives a number comparable across different numbers
of clusters, which is what the k-means objective cannot do: the objective
falls with every added cluster, so it can never say that three is better than
four. The silhouette can, and on six points in three pairs it picks three.
