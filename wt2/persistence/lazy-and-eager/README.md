# Lazy and eager loading

Three parents with two children each, counted by a store that records every
query.

| strategy | children touched | queries | rows read |
|---|---|---|---|
| lazy | no | 1 | 3 |
| lazy | yes | 4 | 9 |
| eager | no | 4 | 9 |
| join fetch | yes | 1 | 6 |

The second row is the n+1 problem: one query for the parents and one per
parent for the children. It does not appear in a test with a single parent
and it appears at once against real data, which is why it is usually found in
production.

The third row is the cost of eager loading: the same four queries even though
nothing needed the children.

## The join is not free either

The join reads 6 rows against 9, but each of those rows repeats the parent's
columns. Three parents become three repetitions, and with more children per
parent the repetition grows. Fewer queries and more transferred data is the
trade; batch loading sits between the two.
