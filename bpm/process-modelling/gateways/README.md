# Gateways

Three kinds, and the number of branches each can take:

| Gateway | Branches taken out of n |
|---|---|
| XOR, exclusive | exactly 1 |
| AND, parallel | all n |
| OR, inclusive | any non-empty subset, so 1 to n |

`branches_taken` returns that as a list, which makes the difference between
the three concrete rather than a sentence to remember.

## Matching splits to joins

`matching` follows every branch of a split until it reaches a node with more
than one incoming flow, and reports a pair whose kinds disagree. A parallel
split closed by an exclusive join and an exclusive split closed by a parallel
join are the two classic errors, and both are found here without executing
anything.

## Why the inclusive gateway is the expensive one

With n branches there are 2ⁿ − 1 possible selections, and the join cannot
simply count arriving tokens: it has to know which branches were actually
taken. That is why many engines restrict it or refuse it, and why the
inclusive join needs a look-ahead in the token game while the other two do
not.
