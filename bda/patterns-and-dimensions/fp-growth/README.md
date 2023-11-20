# FP-growth

Apriori reads the database once per level. FP-growth reads it twice, once to
count the items and once to build a prefix tree of the transactions ordered
by frequency, and mines the tree afterwards without touching the data again.

On the twelfth sheet's eight transactions at a support of three:

| | database passes |
|---|---:|
| FP-growth | 2 |
| Apriori | 4 |

The gap is the length of the longest frequent itemset plus one, so it grows
with the patterns rather than with the data, and on a database with long
patterns it is the whole argument for the tree.

The frequency ordering is what makes the tree small: frequent items sit near
the root and are shared by many transactions. The module checks that the
header table is sorted and that the mined itemsets agree with an enumeration
of every subset.
