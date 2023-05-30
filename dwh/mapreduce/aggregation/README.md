# Aggregation

Three kinds of measure, and only two of them can use a combiner.

| kind | example | combinable |
|---|---|---|
| distributive | sum, count, maximum | yes |
| algebraic | mean, variance | after carrying more state |
| holistic | median, exact distinct count | no |

The mean becomes combinable by carrying the sum and the count instead of the
mean, which is the general repair: an algebraic measure is a function of
distributive ones.

A holistic measure has no such decomposition, which is why approximate
distinct counting exists as a separate algorithm rather than as a
optimisation of the exact one.

The combiner is what keeps the shuffle small, and the shuffle is usually the
dominant cost, so this classification decides the run time of a job before
any tuning does.
