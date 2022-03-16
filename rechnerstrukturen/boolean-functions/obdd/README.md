# Ordered binary decision diagrams

A decision tree over the variables in a fixed order, with two reductions
applied until neither applies: **merge** identical subgraphs, and **remove** a
node whose two children are the same node.

The result is **canonical**. Two functions are equal exactly when their reduced
diagrams are identical, so equivalence checking becomes a comparison of
structures rather than a search. That property is why OBDDs took over hardware
verification.

## Measured on the sheet's function

The five-variable function reduces to **7 nodes** against 32 rows in the truth
table, and `count_satisfying` reports 10 accepting assignments by one walk of
those 7 nodes, matching the vector.

## The order is everything

The same function can have a linear diagram in one variable order and an
exponential one in another. For `(a and b) or (c and d)`, the order
`a, b, c, d` gives a smaller diagram than `a, c, b, d`, measured directly, and
finding the best order in general is NP-hard.

## The bug the reduction causes

Removing a node shortens the path, so the depth of a node is no longer its
position in the variable order. A walk that consumes one bit per step then
reads the wrong bits, and it goes wrong on exactly the functions the reduction
helps most. Every node therefore records **which** variable it tests, and the
walk uses that.
