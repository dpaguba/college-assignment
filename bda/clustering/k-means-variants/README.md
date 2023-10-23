# The k-means family

The same loop with four different notions of a centre.

| variant | centre | robust to | accepts |
|---|---|---|---|
| k-means | the mean | nothing | numbers |
| k-medoid | the most central point | outliers | any distance |
| k-median | the coordinatewise median | outliers | numbers |
| k-mode | the most frequent value | not applicable | categories |

The outlier separates them. A single point at a hundred drags a mean centre
most of the way towards it, and a medoid centre stays where it was, because a
medoid has to be one of the actual points.

k-mode is the variant with no arithmetic in it at all: the distance counts
the attributes that differ and the centre takes the most frequent value in
each position, so the method runs on survey answers.

Every variant depends on the initial centres, which is why the result changes
with the seed and why the algorithm is usually run several times.
