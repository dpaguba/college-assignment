# The observation table

What a learner knows about a system it cannot see.

Rows are words that lead somewhere, columns are experiments run from there, and
a cell holds the answer. For Mealy machines the lecture keeps only the **last**
output symbol of `u . v`, which is enough to separate states and keeps the
table readable.

```
               a |    b
-----------------------
  U     eps     0 |    1
  U     a       1 |    0
-----------------------
  U.A   b       0 |    1
  U.A   aa      1 |    0
  U.A   ab      0 |    1
```

## Closed and consistent

**Closed**: every fringe row already appears in the upper part, so every
transition of the hypothesis has a target. Repaired by promoting the offending
fringe word into `U`, which adds a state.

**Consistent**: rows that look equal stay equal after one more symbol.
Repaired by adding a column `symbol + suffix`, which splits two rows that
should never have been equal.

Each repair costs membership queries, and the two together are the whole cost
model of learning.

## The exercise, exactly

Sheet 5 gives `U = {eps}`, `V = {a, b}` and the rows for `eps`, `a` and `b`,
and asks to close the table and build the hypothesis. The module reproduces
that: closing moves `a` into `U`, the table becomes consistent with no extra
columns, and the hypothesis has **two** states.

That hypothesis is wrong, and knowing why is the point of the next task: `M1`
has three states, and the suffix set `{a, b}` cannot tell `q0` from `q2`,
because both answer `a` with 0 and `b` with 1. Only a longer experiment
separates them, which is what the counterexample in [L*](../lstar/) supplies.

## Why the columns always contain the single symbols

The hypothesis reads its **outputs** out of the cells `(u, symbol)`. Without
those columns the transitions would have targets and no labels, so the initial
suffix set is the alphabet itself.
