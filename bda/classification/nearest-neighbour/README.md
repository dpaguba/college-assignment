# Nearest neighbour

Training is storing the data; predicting is finding the closest examples and
taking their majority label. No model is fitted, so the cost moves entirely
to the query.

On the penguin sample, using only the bill length and depth, leave-one-out
accuracy with three neighbours is 0.944. The geometry of the data does the
work.

## The distance carries the assumptions

A feature in grams dominates one in millimetres, so the neighbours depend on
the units and therefore so does the answer. The module shows a pair of
features differing by three orders of magnitude and the same query giving
different neighbours after scaling. Any use of this method includes a
decision about scaling, whether or not it is made deliberately.

A larger k smooths the boundary, which the module demonstrates by adding one
mislabelled point: at k = 1 the query follows it, and at k = 3 it does not.
