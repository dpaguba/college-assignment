# The pumping lemma for context-free languages

```
z = u v w x y     with |vwx| <= n, |vx| >= 1, and u v^i w x^i y in L
```

Two pieces are pumped **together**, and that is the whole difference from the
regular version. A context-free language can keep two counts in step; it cannot
keep three.

The proof is the parse tree. In Chomsky normal form a long enough word forces a
root-to-leaf path deeper than the number of variables, so some variable repeats
on it, and the subtree between the two occurrences can be inserted again or cut
out.

## Why the case analysis is longer

Four cut points instead of two, so the adversary has many more moves. For
`a^3 b^3 c^3` against n = 3 there are **121** allowed decompositions, and the
proof has to defeat every one of them. The module enumerates and defeats them,
which is what makes the transcript a real case analysis rather than a sketch.

Verified on the two standard languages: `a^n b^n c^n` and `{ww}`.

The second is the more interesting one. A stack reverses what it stores, so a
pushdown automaton can check `w w^R` and not `w w`; the stack is a stack, not a
queue. That single observation is worth more than the pumping proof.

## The control

`survives_pumping` runs the game on `a^n b^n`, which **is** context-free, and
checks that a surviving decomposition exists. Without it a bug in the search
would prove every language non-context-free, with a transcript that looks just
as convincing.
