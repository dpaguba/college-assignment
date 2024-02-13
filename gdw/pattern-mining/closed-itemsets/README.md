# Closed and maximal itemsets

Two ways to keep fewer itemsets.

| | count on the example |
|---|---:|
| frequent | 7 |
| closed | 7 |
| maximal | 1 |

An itemset is closed when no superset has the same support, and maximal when
no superset is frequent. Every maximal itemset is closed, so the families
shrink in that order.

The difference is what survives the compression. The closed itemsets
determine the support of every frequent itemset, since the support of a set
is the largest support among the closed sets containing it, and the module
verifies that for every frequent itemset. The maximal ones determine only
which sets are frequent, so they compress much harder and lose the counts.

On this data the closed family saves nothing and the maximal family reduces
seven sets to one, which is the trade in its extreme form.
