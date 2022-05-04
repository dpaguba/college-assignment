# Subset sum and partition

Can a target be hit exactly with these numbers, and can they split in half.

| | |
|---|---|
| Time | O(n · target) |
| Space | O(target) |
| Table shape | capacity |

## The idea

The knapsack recurrence with the value dropped: only reachability matters. A boolean
per achievable sum, and each number either extends a reachable sum or does not.

Partition is the same question in different words. An odd total can never split,
which costs nothing to check. And if a subset sums to half the total, the rest sums
to the other half automatically, so only one side has to be found.

## The recurrence

```
reachable(s) = reachable(s) or reachable(s - value)
```

## What is worth noticing

Subset sum is one of Karp's original 21 NP-complete problems, and this algorithm
does not contradict that: the table is `target` wide while the target needs only
log(target) bits to write down. Pseudo-polynomial again.

Recognising that a new problem is an old one in different words is the skill this
pair demonstrates. Partition, subset sum and knapsack are the same algorithm three
times.
