# Closed and maximal itemsets

The twelfth sheet's answer, reproduced:

| | count | |
|---|---:|---|
| frequent | 13 | |
| closed | 10 | {C}, {D}, {E}, {F}, {AE}, {DE}, {DF}, {EF}, {ACE}, {DEF} |
| maximal | 2 | {ACE}, {DEF} |

The singleton A is frequent and not closed, and the module says why: A and E
occur in exactly the same transactions, so {AE} has the same support and
listing A separately adds nothing.

Two maximal itemsets summarise all thirteen: every frequent itemset is a
subset of {ACE} or of {DEF}. That is the strongest compression and it loses
the supports, while the closed family keeps them and compresses less. Which
to store depends on whether the counts will be needed again.
