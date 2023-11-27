# Clustering

| Topic | |
|---|---|
| [k-means-variants](k-means-variants/) | four notions of a centre |
| [silhouette](silhouette/) | how well each point sits |
| [expectation-maximisation](expectation-maximisation/) | soft membership |
| [density-based](density-based/) | clusters of any shape |
| [hierarchical](hierarchical/) | the whole tree |

Chapter four. The basic k-means is in
[gdw/learning/clustering](../../gdw/learning/clustering/); this block is
about what the variants buy.

Three measured contrasts carry it. A medoid centre ignores an outlier that
moves a mean centre most of the way to it. The silhouette can compare two
clusterings with different numbers of clusters and the k-means objective
cannot. And on two concentric rings, DBSCAN finds both and k-means puts 18 of
36 points on the wrong side.
