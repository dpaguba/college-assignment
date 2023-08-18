# Thresholds

The z-score and the interquartile rule, and two datasets on which the first
fails.

## The outlier hides itself

In 10, 11, 9, 10, 12, 11, 10, 9, **200** the 200 has a z-score of 2.83, under
the usual threshold of 3, so nothing is reported. Mean and deviation are
computed from the same data the outlier is in; it raises both, and thereby
makes itself less conspicuous. The interquartile rule finds it, because the
quartiles do not count the edge.

## Two populations defeat the threshold entirely

With half the points around 0 and half around 20, the mean lands at 10, in the
gap where almost nothing is, and the deviation is large. A point inserted at
exactly 10 belongs to neither cluster and is reported by nothing: the z-score
flags zero points in the whole dataset.

That is the case for which the local methods of the next module exist.
