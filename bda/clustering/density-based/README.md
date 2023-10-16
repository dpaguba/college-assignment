# Density-based clustering

A point is a core point when enough neighbours lie within a radius, core
points that reach each other form a cluster, and a point that reaches none is
noise. The number of clusters is not a parameter.

Two concentric rings are the case that separates the methods:

| | |
|---|---|
| DBSCAN | 2 clusters, the rings |
| k-means with two clusters | 18 of 36 points on the wrong side |

k-means can only draw straight boundaries, so it cuts both rings in half.
DBSCAN follows the density and separates them, because the rings are dense
along their own circumference and empty in between.

The difficulty moves rather than disappearing. The radius decides everything:
too small and every point is noise, too large and everything is one cluster,
and the module shows both ends on the same four points.
