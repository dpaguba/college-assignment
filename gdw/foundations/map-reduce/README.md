# Map and reduce

Split the data, map each part, combine with the reduce. The framework decides
the order, so the reduce has to be associative: summing works, averaging does
not.

The repair is standard and worth stating as the pattern: carry the sum and
the count instead of the mean, combine those, and divide at the end. What was
not associative becomes associative by carrying more state.

A combiner reduces locally before the data crosses the network, which turns
eight pairs into two on the small example and leaves the result unchanged.
That is the same argument at a different level: the operation is associative,
so it may be applied early.

The module checks that partitioning the input three ways gives exactly the
same word counts, which is the property the whole model rests on.
