# k-means

Pick k starting centres, assign every point to the nearest one, move each
centre to the mean of its points, repeat. The objective never rises during
the iteration, which the module records as a history and the tests check.

## The answer depends on where it starts

The exercise asks whether repeated calls always give the same result. They do
not. On a set built for it, twenty different seeds produce several distinct
objective values, and the module reports how many.

Against the exhaustive optimum, computed by trying every assignment of the
points to k groups, the algorithm with eight restarts still ends above the
optimum in 3 of 40 random instances. It is a local method; restarting is the
only defence and it is not a guarantee.

## Choosing k

The objective falls with every added cluster, so it cannot choose k on its
own. The elbow and the silhouette coefficient are the two usual answers; the
silhouette is implemented next door.
