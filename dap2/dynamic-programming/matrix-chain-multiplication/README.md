# Matrix chain multiplication

Where to put the brackets.

| | |
|---|---|
| Time | O(n³) |
| Space | O(n²) |
| Table shape | interval |

## The idea

Matrix multiplication is associative, so the result never changes and the cost
changes enormously. For 10x30, 30x5, 5x60:

```
((A1 A2) A3)  costs 10·30·5 + 10·5·60  =  4500
(A1 (A2 A3))  costs 30·5·60 + 10·30·60 = 27000
```

Six times the work for the same answer. The number of bracketings is the Catalan
numbers, which grow faster than 2ⁿ.

## The recurrence

```
cost(i, j) = min over k of (cost(i, k) + cost(k+1, j) + d[i]·d[k+1]·d[j+1])
```

## What is worth noticing

The recurrence is over **intervals** rather than prefixes, which is a new shape. The
loops iterate by chain length rather than by position, because a longer interval
needs every shorter one to be ready first.

That shape reappears in optimal binary search trees, polygon triangulation and the
CYK parsing algorithm.
