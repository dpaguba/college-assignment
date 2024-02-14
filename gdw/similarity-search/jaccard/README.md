# Jaccard similarity

The intersection over the union: one for identical sets, zero for disjoint
ones, and one half for `{1,2,3}` against `{2,3,4}`.

One minus it is a metric, so the triangle inequality holds, which the module
checks over every triple of eight sample sets. That matters more than it
looks: without the inequality, a neighbourhood is not a well-behaved notion
and none of the indexing methods in the next modules can be justified.

Two empty sets are defined as identical here. The formula gives zero over
zero, so the value is a convention, and stating it is better than letting the
implementation decide by accident.
