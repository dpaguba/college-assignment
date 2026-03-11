# Linear arithmetic

Deciding the arithmetic side conditions, which is the T in SMT.

A SAT solver decides propositional structure. It knows nothing about `s' = s / 2`
or `x mod 2 = 0`, and every question in this folder ends in one of those. Two
procedures are here, and they cover different ground.

## Fourier-Motzkin, complete over the rationals

Eliminate one variable at a time: split the inequalities into those bounding
it from above and from below, replace each opposing pair by the combined bound
with the variable gone, repeat, then check what is left on constants.

Complete for conjunctions of linear inequalities over the rationals, and
needs no bounds at all. The catch is in the word rationals: `2x = 1` is
satisfiable there and has no integer solution. Over the integers this is a
sound test for **un**satisfiability only.

Eliminating a variable can square the number of inequalities, so the cost is
doubly exponential in the worst case. It is a decision procedure that can be
read, not a solver to build on.

## Bounded search, complete inside its box

Backtracking over integer domains, with a conjunct evaluated the moment all
its variables are bound so a false one prunes the subtree. It handles anything
the expression language can express, including `mod`, integer division and
products of variables.

The bounds are where the difficulty is parked, and the accurate statement of what
they buy: an answer computed with them is an answer about the states inside
them. Presburger arithmetic, the linear integer theory, is decidable but
expensive; add multiplication of variables and it becomes undecidable outright.

## How the two are used

Bounded model checking and inductive invariants use the search, because they
need integer models to print as counterexamples. Symbolic execution prunes
with Fourier-Motzkin first, since a path condition with no rational solution
has no integer solution either, so nothing reachable is ever discarded.

## Verification

200 random linear systems against exhaustive enumeration, the rational versus
integer gap demonstrated on `2x = 1`, and the non-linear fallback on
`x * y = 12`.
