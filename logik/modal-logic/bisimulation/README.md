# Bisimulation

Two worlds are bisimilar when they carry the same atoms and every step from one
can be matched by a step from the other, in both directions, forever. The point
of the definition is a theorem: **bisimilar worlds satisfy exactly the same
modal formulas**.

That theorem is what makes modal logic a logic of behaviour. It can never see
the identity or the number of states, only what can happen, which is why a
transition system and its minimisation are indistinguishable to it.

## A loop and its unwinding

A two-world structure `1 -> 2 -> 2` with `A` everywhere is bisimilar to a
single world with a self-loop. Every formula tried, `A`, `[]A`, `<>A`, `<><>A`,
`[]<>A`, `[](A & <>A)`, agrees on both. Unwinding the first four levels
produces a tree, verified to be one, and the tree agrees with the original on
the same formulas.

## What breaks it

| change | bisimilar | formula that separates them |
|---|---|---|
| different labels | no | `A` |
| remove the successor | no | `<>A` |

The second row is the useful one: bisimilarity fails exactly when some modal
formula distinguishes the worlds, and the search finds that formula.

## Greatest fixed point, not least

The relation is computed by starting with every pair that has equal labels and
removing pairs whose steps cannot be matched, until nothing changes. Starting
from nothing and growing would give the empty relation, which satisfies the
definition vacuously and relates nothing. The direction of the fixed point is
the definition, not an implementation choice.

`quotient` merges bisimilar worlds, which is the modal analogue of minimising
an automaton and the reason bisimulation is computed in practice.
