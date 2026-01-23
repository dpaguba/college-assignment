# Isolation forest

Split the data at random and see how deep a point has to go before it stands
alone. Outliers are cut off early, and no distance and no density estimate is
needed anywhere.

## The normalising term

The measured depth is divided by the average path length of a random binary
search tree, `2·H(n−1) − 2(n−1)/n`. Without it, depths from trees built on
different sample sizes could not be compared. The implementation is checked
against that definition for every size from 2 to 300.

## Two trees are not enough

| trees | spread of the score for the same point |
|---:|---:|
| 3 | 0.036 |
| 60 | **0.009** |

Every tree splits at random, so a single one says almost nothing; only the
average is stable. That is the actual cost of the method, and it is paid in
trees rather than in data.

## Why the sample stays small

Each tree sees a few hundred points at most, and more would make the result
worse: in a large sample there are enough points near an outlier to bury it in
the crowd. The cost therefore does not grow with the size of the dataset,
which is the property that makes the method practical.
