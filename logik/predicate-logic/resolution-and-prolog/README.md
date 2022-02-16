# First-order resolution and Prolog

Ground resolution instantiates everything first. Robinson's insight was that
instantiating can be **postponed**: resolve whenever two literals unify, and let
the most general unifier decide how much to instantiate. Complete, and
enormously more efficient, because no instance is built that the proof does not
need.

| clauses | refutable |
|---|---|
| `P(x)`, `!P(a)` | yes, `x` unifies with `a` |
| `P(f(x))`, `!P(a)` | no, `f(x)` never equals `a` |
| `P(x) \| Q(x)`, `!P(y)`, `!Q(a)` | yes, and only after renaming apart |

The third row is the one that fails silently when renaming is forgotten. Two
clauses that happen to use the same variable name are not talking about the
same thing, and resolving them unrenamed derives nonsense. The step is
invisible in a written proof, which is why it is the most common mistake in one.

## Prolog is this rule, restricted

SLD resolution is resolution on Horn clauses with a fixed selection strategy,
and it is a programming language: definite clauses are the program, a negative
clause is the query, and the substitution accumulated along the refutation is
the answer.

    parent(anna, bea).
    parent(bea, cara).
    grandparent(X, Z) :- parent(X, Y), parent(Y, Z).

    ?- grandparent(anna, Q).      Q = cara

Recursion works the same way, and needs a depth bound here because the search
is depth first: `path(X,Z) :- edge(X,Y), path(Y,Z)` finds `b` and `c` from `a`,
and would not terminate on a cyclic graph without one. Real Prolog has the same
problem and the same non-answer.

## Clause order is part of the program

The clauses are tried top to bottom, so a Prolog program is a **sequence** of
statements rather than a set of them, and swapping two clauses can turn a
terminating program into a non-terminating one. That is the gap between the
logical reading and the operational one, and it is the first thing a logic
programming course has to teach.

## Two naming conventions on purpose

First-order terms use the lecture's convention, lower-case letters from the end
of the alphabet are variables. Prolog uses capitals. Both are implemented
separately rather than unified behind a shared helper, because the clash is
real and hiding it would make the Prolog module quietly wrong for a term like
`X`.
