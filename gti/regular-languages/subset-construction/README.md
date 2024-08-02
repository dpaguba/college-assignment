# The subset construction

An NFA becomes a DFA. A state of the DFA is a **set** of NFA states: exactly
the set the NFA could be in after reading the word so far. Determinism is
recovered by tracking every possibility at once instead of guessing.

Only the reachable subsets are built, which is what keeps it usable in
practice.

## The blow-up is real

The language "the k-th symbol from the end is an `a`" is accepted by an NFA
with k+1 states, which guesses where the end is, and by no DFA with fewer than
2^k, because a deterministic machine has to remember the last k symbols.

`blowup_example` builds it, and the numbers come out exactly:

| k | NFA states | DFA states | 2^k |
|---|---|---|---|
| 2 | 3 | 4 | 4 |
| 3 | 4 | 8 | 8 |
| 4 | 5 | 16 | 16 |
| 5 | 6 | 32 | 32 |

So the exponential bound is tight, and it is not an artefact of the
construction: no cleverer determinisation can do better on this family.

## The table

`construction_table` produces the row-per-subset table the exercises ask to be
filled in by hand, which is the manual version of the same algorithm.
