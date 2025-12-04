# Dimensionality reduction

Keep the k strongest axes and project. The price is known in advance: the mean
squared reconstruction error is exactly the sum of the discarded eigenvalues.
Verified against `numpy.linalg.eigvalsh` on the covariance matrix, for every k
from 1 to the dimension, over 60 random datasets of varying shape.

That identity is why the slide can say the representation is compact "without
great loss of information": the loss is not estimated, it is read off the
eigenvalue list before anything is computed.

## Variance is not information

The reduction keeps the directions with the largest variance. That is the
relevant information only if the task depends on spread. A feature that
separates two classes cleanly but varies little is discarded first, and the
method cannot help it: principal component analysis never sees the categories.

## How k gets chosen

The slide says k is often determined empirically and leaves open by what. In
practice it is one of three:

| Rule | What it measures |
|---|---|
| a knee in the eigenvalue curve | the shape of the data |
| a fixed share of variance kept | the shape of the data |
| the error rate of the actual task | the task |

Only the third measures the thing that matters, and only the third needs the
task itself. The first two are cheaper and answer a different question.
