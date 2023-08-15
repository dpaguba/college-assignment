# Distance and density

The distance to the k-th neighbour is the simple measure: whoever is far from
their neighbours is suspect. It works while every region has the same density.

The local outlier factor compares the density around a point with the density
around its neighbours. A value near one means it sits as densely as they do;
well above one means it sits more thinly than its own surroundings.

## The measurement

Sixty points in a tight cluster, thirty in a loose one, and a point inserted
just outside the tight cluster. By distance to its fifth neighbour it ranks
**14th of 92**, because in the loose cluster all distances are larger anyway.
By local factor it ranks **2nd**, with a factor of 6.5.

The absolute distance measures against the whole dataset; the factor measures
against the neighbourhood, and only the second question is the one being
asked.
