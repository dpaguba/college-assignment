# The Herbrand universe and ground resolution

Herbrand's theorem: a formula in Skolem form is unsatisfiable exactly when some
**finite** set of ground instances of its matrix is unsatisfiable as a
propositional formula. An infinite question about all structures becomes a
sequence of finite propositional ones.

The instances range over the Herbrand universe, all ground terms buildable from
the signature.

## The published universe

For constants `a, b` and function symbols `f/1, g/2`, the terms with at most one
function symbol are exactly the eight the solution lists:

    a  b  f(a)  f(b)  g(a,a)  g(a,b)  g(b,a)  g(b,b)

and the growth is the reason first-order proving is hard:

| nesting depth | terms |
|---|---|
| 0 | 2 |
| 1 | 8 |
| 2 | **74** |

With any function symbol the universe is infinite, so the sequence of
propositional questions never ends. That is semi-decidability made concrete:
`refute_with_expansion` terminates on unsatisfiable input and runs forever
deepening the universe on satisfiable input.

## A signature with no constant gets one

Otherwise the universe would be empty and the theorem would say nothing about
the formula. Inventing a constant is the standard convention and is what makes
the statement uniform.

## Once ground, it is propositional

Ground clauses have no variables left, so there is nothing to unify and the
refutation is exactly the propositional one from
[propositional-logic/resolution](../../propositional-logic/resolution/). The
whole content of the first-order case is choosing which instances to generate,
which is what [resolution-and-prolog](../resolution-and-prolog/) improves on by
not generating them at all.
