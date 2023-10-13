# Pruning

A tree grown until its leaves are pure fits the noise. On 300 rows with 15
percent of the labels flipped:

| | training | test | nodes |
|---|---:|---:|---:|
| unpruned | 0.94 | 0.75 | 123 |
| minimum leaf of five | 0.90 | 0.76 | 92 |

Four points of training accuracy traded for one of test accuracy and a
quarter of the tree. The direction is what matters: the removed structure was
noise, so removing it costs on the data it was fitted to and gains on the
data it was not.

The unpruned tree does not even reach 1.0, because rows with identical
attribute values carry different labels after the flipping, and no tree can
separate them. That is the irreducible part of the error, and it is exactly
what a tree that keeps growing is trying to fit.
