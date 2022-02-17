# Unification

Two terms unify when a substitution makes them identical. Robinson's algorithm
walks them in parallel with three cases: matching symbols recurse, a variable
binds, anything else fails.

| terms | result |
|---|---|
| `f(x,g(y))` and `f(a,g(b))` | `{x: a, y: b}` |
| `p(x,x)` and `p(y,f(a))` | `{x: y, y: f(a)}` |
| `f(a)` and `g(a)` | none, different symbols |
| `f(a)` and `f(a,b)` | none, different arities |
| `x` and `f(x)` | **none, occurs check** |

## The occurs check

Unifying `x` with `f(x)` has no finite solution. Skipping the test produces a
cyclic term that makes the prover loop or crash later, and Prolog systems omit
it for speed and document that they are unsound as a result. It is one line and
it is the difference between an algorithm and an algorithm that usually works.

## Most general

The unifier returned is the most general one: every other unifier is an
instance of it. That property is what makes resolution with unification
complete, while resolution over arbitrary ground instances is only complete in
the limit, and it is checked here rather than asserted.

## A naming convention with teeth

Variables are lower-case letters from the end of the alphabet, optionally
followed by digits. The digits are not decoration: resolution renames clauses
apart by appending them, and an earlier version recognised only single letters,
so every renamed variable silently became a constant and every unification
after the first rename failed. Every test written against that version passed,
because they all used unrenamed terms.
