# Cyclomatic complexity

McCabe's measure, computed from the control flow graph.

```
CC = e - n + 2p
```

with `e` edges, `n` nodes, `p` connected components. The lecture's example has
six nodes, six edges and one component, so `CC = 2`: the loop is entered or it
is not.

## What it measures

The number of independent paths, which is a lower bound on the number of test
cases needed for branch coverage. That is the practical use: it is a testing
budget, not a beauty score.

Straight-line code of any length scores 1. Every test adds one. On a
structured program the count of decisions plus one gives the same number,
which is why both formulations are in the module and why they can disagree
only on graphs that did not come from structured code.

## What it misses

A `switch` with twenty cases scores twenty and reads fine. Two nested loops
sharing a flag score four and do not. The measure counts branching, and
branching is one source of difficulty among several: nesting depth, data flow
and naming do not appear in it at all.

It is also trivially gamed. Splitting one function into three does not change
how hard the code is, and it lowers every per-function score.

## Verification

`CC = 2` on the lecture example, `CC = 1` on straight-line code, and 3 on a
loop containing a conditional, all computed from the graph rather than from a
count of keywords.
