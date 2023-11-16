# The curse of dimensionality

Distances stop distinguishing. The relative spread of the pairwise distances
between random points:

| dimensions | 2 | 10 | 50 | 200 |
|---|---:|---:|---:|---:|
| spread over mean | 0.475 | 0.192 | 0.084 | 0.041 |

At 200 dimensions every pair is about equally far apart, so a nearest
neighbour is barely nearer than a farthest one and any method resting on that
difference is resting on almost nothing.

The volume argument says it geometrically. The ball inscribed in a cube fills:

| dimensions | 2 | 3 | 5 | 10 |
|---|---:|---:|---:|---:|
| share of the cube | 0.785 | 0.524 | 0.164 | 0.002 |

Almost all of a high dimensional cube is in its corners, so a sample drawn
uniformly is nowhere near the middle, and a grid covering the space at ten
points per axis needs a thousand points in three dimensions and 10²⁰ in
twenty.
