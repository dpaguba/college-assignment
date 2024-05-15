# DBSCAN

A point is a core point when its ε-neighbourhood holds at least `min_points`
points. Clusters grow from core points through density reachability; a point
in the neighbourhood of a core point that is not itself core is a border
point; everything else is noise.

The result is checked against an independent computation: the clusters must
be exactly the connected components of the graph on core points that are
within ε of each other, built here with a union-find. They agree on 40 random
point sets.

## What it does that k-means cannot

It finds the number of clusters itself. The same parameters applied to data
with two groups and to data with three return two and three, which the module
verifies. It also refuses to assign the point in the middle of nowhere: the
lone point at (5, 5) comes back as noise rather than being forced into a
cluster.

The price is the two parameters. Too small an ε and everything is noise; too
large and everything is one cluster, which the tests show by pushing ε to
100 and getting a single label.
