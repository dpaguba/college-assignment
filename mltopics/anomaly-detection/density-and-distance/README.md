# Distance and local density

The distance to the k-th nearest neighbour is the simplest usable anomaly
score: whoever sits far from their neighbours is unusual. It measures density
on one scale everywhere, and that is exactly where it fails.

## The case the local factor was built for

Two clusters, one tight and one wide, and a point at the edge of the tight
one.

| measure | rank of the planted point |
|---|---:|
| k-th nearest distance | **200 of 401** |
| local outlier factor | **1 of 401** |

Globally, the planted point sits closer to its neighbours than many ordinary
members of the wide cluster, so a global measure never sees it. The local
factor compares a point's reachable density with that of its own neighbours,
and it finds the point immediately.

On a uniform cloud the factor has a median of 1.04, which is the sanity check:
a value near one means "as dense as my surroundings".

## What both assume

That proximity in the chosen distance means belonging. In many dimensions that
stops being true because all distances converge; on time series it is only
true with a distance that tolerates a shift; on mixed features it is only true
after the scales have been matched.

The method never checks the assumption and always returns a ranking.
