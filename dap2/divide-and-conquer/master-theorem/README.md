# The Master theorem

Reading the cost of a divide and conquer recurrence.

| | |
|---|---|
| Time | constant, it is a solver |
| Recurrence | `T(n) = a·T(n/b) + Theta(n^k)` |
| Master theorem | all three |

## The idea

Almost every algorithm in this folder has that shape: `a` subproblems of size n/b,
plus n^k work to split and combine. The theorem says the answer depends on one
comparison, between k and log_b(a).

log_b(a) is the cost of the leaves, how much work the recursion produces at the
bottom. n^k is the cost of one level of combining. Whichever grows faster decides,
and when they tie a logarithmic factor appears for the log_b(n) levels.

| | | |
|---|---|---|
| k < log_b(a) | the leaves dominate | Θ(n^log_b(a)) |
| k = log_b(a) | every level costs the same | Θ(n^k log n) |
| k > log_b(a) | the top dominates | Θ(n^k) |

## What is worth noticing

Reading the cases as "who does the work" rather than as three formulas is what makes
them memorable, and it explains at a glance why Karatsuba and Strassen matter: both
reduce `a` while leaving b and k alone, which lowers log_b(a) and therefore the whole
bound.

The solver returns the case, the bound and the reason, so the recurrences in this
folder can be checked rather than recalled:

```
solve(a=2, b=2, k=1)  merge sort            Theta(n^1 log n)
solve(a=3, b=2, k=1)  Karatsuba             Theta(n^1.585)
solve(a=8, b=2, k=2)  blocks, naive         Theta(n^3)
solve(a=7, b=2, k=2)  Strassen              Theta(n^2.807)
```
