# Symbolic execution

Run the program on symbols instead of numbers and collect the conditions.

The lecture gives the same seven rules as the concrete semantics with two
changes: variables map to **expressions over symbols**, and each branch
carries a **path condition**, the conjunction of the tests taken to reach it.

```
<if b then S1 else S2, v, f> => <S1, v, f and b>       if satisfiable
<if b then S1 else S2, v, f> => <S2, v, f and not b>   if satisfiable
```

Both rules can apply, so execution becomes a tree.

## What it produces

On the lecture's own example:

```
[y := x + 100]1; if [y > 200]2 then [z := 1]3 else [z := 2]4

labels [1, 2, 3]   condition: X + 100 > 200      state: y = X+100, z = 1
labels [1, 2, 4]   condition: !(X + 100 > 200)   state: y = X+100, z = 2
```

Solving each condition gives an input that provably reaches that leaf:
`X = 101` and `X = -410`. That is automatic test generation, and it is what
KLEE and its relatives do to real binaries.

## Pruning

A branch whose path condition is unsatisfiable is dropped, so the tree
contains only paths that can actually happen. On the nested example
`x > 0 and x < 0` the pruned tree has two leaves and the unpruned one three,
and the missing leaf is code no input can reach.

Pruning uses Fourier-Motzkin for linear conditions, which needs no bounds and
never discards a reachable path. Non-linear conditions fall back to the
bounded search.

## The bounds trap

The first version of this module used a fixed window of [-32, 32] for
feasibility, and silently dropped the `X + 100 > 200` branch as impossible: no
solution exists in that window, and plenty exist outside it. A pruning step
that is too narrow does not fail loudly, it reports fewer paths. Bounds are now
derived from the constants in the condition, and the linear case avoids them
entirely.

## Loops

Each iteration is another unrolling, so a loop with an unbounded trip count has
infinitely many paths. The depth bound makes the search finite, and a path that
hits it is returned marked incomplete rather than dropped, so "no more
behaviour" and "we stopped looking" stay distinguishable. That distinction is
the whole problem of symbolic execution at scale, and it has no clean answer.
