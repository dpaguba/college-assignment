# Materialized views

An aggregate over a set of dimensions answers any query over a subset of
them: summing further is always possible and splitting is not. The aggregates
therefore form a lattice, and materialising a node makes every node below it
cheap.

The base cube sits at the top and answers everything, at the highest storage
and maintenance cost. Every load has to update every materialised view, so
five views and thirty loads a month are 150 updates, and that recurring cost
is what limits the selection rather than the disk.

The cost of a query is the size of the smallest view that can answer it,
which is the model the next module optimises over.
