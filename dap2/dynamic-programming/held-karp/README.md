# Held-Karp

The travelling salesman, exactly, in exponential rather than factorial time.

| | |
|---|---|
| Time | O(n² · 2ⁿ) |
| Space | O(n · 2ⁿ) |
| Table shape | over subsets |

## The idea

Trying every order costs (n-1)!, which is 3.6 million at 11 cities and out of reach
by 15. Held and Karp's 1962 algorithm gets it to O(n²·2ⁿ): 2²⁰ is a million where
19! is 121 quadrillion.

The state is a **set** rather than an index, which is what makes this different from
everything else here. The same subset reached by different orders is computed once
instead of once per order, and that collapse from orders to subsets is the whole
saving.

## The recurrence

```
best(S, j) = min over i in S of (best(S - {j}, i) + distance(i, j))
```

## What is worth noticing

It remains the fastest known exact algorithm for the general travelling salesman
problem. Sixty years have not improved the exponent, which is itself worth knowing:
this is what "better than brute force, but not much" looks like when the problem is
NP-hard.

Above twenty cities the table stops fitting in memory, so the implementation refuses
rather than thrashing.
