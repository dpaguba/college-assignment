# Mealy machines

The models the course tests systems against.

A Mealy machine answers every input symbol with an output symbol, so a word of
length n produces a word of length n. That is what makes it the natural model
of a reactive component: every call gets an answer.

```
M1: start q0
  state | on a | on b
  q0    | q1/0 | q2/1
  q1    | q1/1 | q2/0
  q2    | q0/0 | q2/1
```

## Access sequences

`reachable` returns one shortest word per state, found by breadth-first
search: `q0` by the empty word, `q1` by `a`, `q2` by `b`. Every test suite in
the next folder is built on them, because testing something about a state means
getting there first.

## Distinguishing two machines

`distinguishing_word` walks pairs of states breadth-first, which is the
product construction. Two machines disagree exactly when some reachable pair
answers one symbol differently, and taking the first pair found gives a
**shortest** counterexample.

For finite machines this decides equivalence: the number of state pairs is
finite, so the search either finds a difference or exhausts them. On the
exercise's hypothesis against `M3` it returns `abaa`, and the two outputs
differ in the last symbol.

## Minimisation

Partition refinement, Moore's algorithm: start with states grouped by their
output behaviour and split whenever two states in a group lead into different
groups. The partition it stops at is the coarsest one that respects behaviour,
so the quotient is the smallest machine with the same behaviour.

Minimisation matters for learning: the machine [L*](../lstar/) produces is
minimal by construction, because its states are distinct rows of the
observation table, and no two distinct rows can be behaviourally equal.

## Verification

The sheet's own numbers: `M1` answers `abba` with `0010` and `baab` with
`1000`, which is what the marked solution gives, and the access sequences match
the solution's `alpha(q0) = eps, alpha(q1) = a, alpha(q2) = b`.
