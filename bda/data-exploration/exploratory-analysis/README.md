# Exploratory analysis

Looking at the data before modelling it.

A histogram depends on the number of bins, so two pictures of the same data
can suggest different distributions. A scatter shows a grouping that a single
correlation cannot: on the penguin measurements the variation between species
is larger than the variation within them, and the module computes both parts.

## Simpson's paradox

The module builds a data set where each of two groups shows a negative
relation and the pooled data shows a positive one. Both computations are
correct and reporting only one of them is misleading, which is the argument
for looking at the groups before summarising over them.
