# Fibonacci

The same recurrence written four ways, at four different costs.

| | |
|---|---|
| Time | O(φⁿ) naive, O(n) otherwise |
| Space | O(n) tabulated, O(1) rolling |
| Table shape | linear |

## The idea

F(n) = F(n-1) + F(n-2) reads exactly like the mathematics and costs exponentially,
because F(n-2) is recomputed inside F(n-1) and again beside it, all the way down.

**Measured here:** computing F(30) naively makes 2,692,537 calls to produce at most
31 distinct values. With memoisation it makes 31. That gap between calls and
distinct answers is the entire motivation for dynamic programming.

## The recurrence

```
F(0) = 0,  F(1) = 1,  F(n) = F(n-1) + F(n-2)
```

## What is worth noticing

Four versions sit side by side deliberately, because they are the four stages every
problem in this folder goes through.

**Naive** is the definition. **Memoised** is the same recursion with answers cached,
top down: only what is needed gets computed, at the cost of stack depth.
**Tabulated** fills forward from the base cases, bottom up: no recursion, and the
fill order becomes visible. **Rolling** is what seeing the fill order buys, because
nothing older than two steps is ever read again, so the table can go.

That last move, noticing which part of the table is still live, shrinks knapsack,
LCS and edit distance from a full grid to one or two rows the same way.
