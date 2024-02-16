# Locality sensitive hashing

Split the signature into bands of rows and call two documents candidates when
they agree on a whole band. The probability of that is an S-curve in the
similarity, steep enough to act as a threshold.

With 20 bands of 5 rows:

| similarity | chance of becoming a candidate |
|---|---:|
| 0.4 | 0.19 |
| 0.55 (the threshold) | about 0.5 |
| 0.8 | 1.00 |

The threshold is roughly the number of bands to the power of minus one over
the rows, which is 0.549 here. More bands lower it and more rows raise it, so
the two parameters set where the curve sits and how steep it is.

That is what turns a quadratic problem into a linear one. Comparing every
pair of a hundred documents is 4950 comparisons; banding leaves only the
pairs sharing a band, and for a collection where most pairs are dissimilar
that is a small fraction.
