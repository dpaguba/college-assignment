# Turing machines

A finite control, an infinite tape, and a head that reads, writes and moves.
The Church-Turing thesis says this is all computation is, and the evidence is
that every other model anyone proposed accepts exactly the same languages.

## The two example machines

`a^n b^n` and `a^n b^n c^n`, both by crossing off one symbol of each kind per
round. The second is the point: it is the language the
[CFL pumping lemma](../../context-free/cfl-pumping-lemma/) rules out one level
down, and the tape does it without effort.

Both were wrong when first written, and both accepted **too much**: the scan
phase skipped the crossed-off symbols and then happily picked up a stray `a`
further right, so `abab` was accepted as if it were `aabb`. The fix is a
separate verification phase, and the lesson is that a machine which accepts all
the intended words is not thereby correct.

## Halting is not a decision

`run` returns `accept`, `reject` or `limit`, and the third is the accurate
answer. Nothing here can tell a slow computation from a non-terminating one,
which is the halting problem stated as a limitation of the simulator rather
than as a theorem.

## Computing, not only deciding

`successor` adds one to a binary number and the answer is read off the tape.
That is what makes a Turing machine a model of **computation** rather than of
recognition, and every reduction in [reductions](../reductions/) depends on it:
a reduction is a computable function, and this is what computable means here.
