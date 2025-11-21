# Lloyd's algorithm

Two steps alternating: assign every point to its nearest centroid, then set
every centroid to the mean of its points. Neither step can raise the
quantisation error, so the error falls monotonically and the procedure stops.
That it stops at the best point does not follow, and does not happen.

Both conditions from the slide are checked directly: after the assignment
every point sits at its nearest centroid, and after the update every centroid
is the mean of its cluster. Monotonicity is checked over 60 random datasets
with different sizes, dimensions and starting points.

## The local optimum, measured

Four blobs, three centroids, twelve starting points:

| | error |
|---|---:|
| best | 4.5607 |
| worst | 4.7629 |
| spread | 0.2021 |

Five of the twelve reach the best value. In every one of the twelve the
algorithm has arrived somewhere nothing moves any more. The remedy is not a
better stopping rule, it is more starting points, and `best_of` is what that
looks like.

## What the size of the vocabulary decides

Few centroids fold different shapes together and make images more similar than
they are. Many centroids separate finely, but two images of the same word then
land in different classes and the histogram becomes sparsely filled. It is the
same problem as k in the nearest-neighbour rule: the answer only exists
relative to the task.
