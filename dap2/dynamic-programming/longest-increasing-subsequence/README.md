# Longest increasing subsequence

The longest rising run, keeping order but not adjacency.

| | |
|---|---|
| Time | O(n²) or O(n log n) |
| Space | O(n) |
| Table shape | linear |

## The idea

The quadratic version uses the same reframing as Kadane: the longest subsequence
**ending at** position i, found by looking back at every smaller earlier value.

The fast version keeps a different thing entirely: entry k is the smallest value
that can end an increasing subsequence of length k+1. That list is always sorted, so
binary search places each new value, which either extends the list or lowers an
existing tail.

## The recurrence

```
best(i) = 1 + max over j < i with values[j] < values[i] of best(j)
```

## What is worth noticing

Lowering a tail is the part worth pausing on. It changes no answer now and makes
future extensions easier, because a smaller tail accepts more successors.

**The tails list is not itself a valid subsequence.** It is a record of the best
endings, which is why reconstructing the actual sequence needs separate
bookkeeping. Reading the tails out and calling them the answer is the standard bug.

This is patience sorting dealt as in the card game, and the pile count is the
length.
