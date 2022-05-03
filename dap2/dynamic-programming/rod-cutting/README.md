# Rod cutting

Where to cut a rod so the pieces sell for the most.

| | |
|---|---|
| Time | O(n²) |
| Space | O(n) |
| Table shape | linear |

## The idea

A rod of length n can be cut in 2^(n-1) ways, so enumeration is hopeless by twenty.
But the remainder after the first cut is an independent smaller instance of the same
problem, and there are only n distinct remainders.

Exponentially many arrangements, linearly many subproblems. That is optimal
substructure and overlapping subproblems together, which is exactly the pair
dynamic programming needs.

## The recurrence

```
best(n) = max over i of (price[i] + best(n - i))
```

## What is worth noticing

The simplest problem where the state is a single number and the transition is a loop over choices. Knapsack, coin change and longest increasing subsequence all share that shape.
