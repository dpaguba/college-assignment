# Longest common subsequence

The longest order-preserving overlap of two sequences.

| | |
|---|---|
| Time | O(n · m) |
| Space | O(n · m), or O(min(n, m)) rolling |
| Table shape | two sequences |

## The idea

A subsequence keeps the order but not the adjacency, which is far weaker than a
substring and correspondingly harder to search for directly: a sequence has 2ⁿ
subsequences.

The grid is what makes it tractable. Two indices, one per sequence, so there are
only n·m distinct subproblems, each costing one comparison and two lookups.

## The recurrence

```
if left[i] == right[j]:  1 + LCS(i-1, j-1)
otherwise:              max(LCS(i-1, j), LCS(i, j-1))
```

## What is worth noticing

This is what `diff` computes to decide which lines are unchanged, and the same shape
as edit distance and biological sequence alignment.

The rolling version keeps two rows and returns the length only: the path that would
be walked backwards lived in the rows that were discarded. That trade, answer or
reconstruction, recurs throughout this folder. Hirschberg's algorithm gets both, in
linear space and twice the time, by recursing on the midpoint.
