# Clustering

k-means alternates two steps: assign each point to the nearest centre, move
each centre to the mean of its points. Both steps lower the objective, so it
terminates, and the module checks that the objective never rises.

Neither step looks beyond the current assignment, so it terminates at a local
optimum that depends on the start. Different seeds give different answers on
the same data, which is why the algorithm is normally run several times and
the best result kept.

The number of clusters is not found by the method. The objective falls with
every additional cluster, always, so the curve has no minimum and the elbow
is a judgement. The module returns the curve rather than a number, which is
the correct output for a question the method cannot answer.

Hierarchical clustering avoids the choice by producing the whole tree of
merges, and moves the decision to where the tree is cut.
