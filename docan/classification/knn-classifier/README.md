# k nearest neighbours

Find the k nearest training vectors, let them vote, and on a tie let the
nearest of the tied classes decide. Verified against a full sort of all
distances over 200 random problems.

## The tie-breaking rule is a decision

A tie has to be broken somehow, and the usual suggestions are to pick at
random or to take the first label in the training order. Both make the answer
depend on something that has nothing to do with the data. The nearest
neighbour among the tied classes is at least a property of the query, and it
gives the same answer every time.

## What k does

| k | Behaviour |
|---|---|
| 1 | follows every outlier, and is always right on its own training data |
| N | always answers the most frequent category |
| between | can only be measured |

The middle row is the whole point: there is no derivation, only measurement,
and the measurement has to be made on data that were not used to choose k.

## Error rate and confusion matrix

The error rate says how often the classifier is wrong. The matrix says at
what. Two methods with the same error rate can differ completely here, and for
the question of what to fix, only the matrix helps.
