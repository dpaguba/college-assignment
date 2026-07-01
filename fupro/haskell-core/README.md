# Haskell core

| Topic | |
|---|---|
| [algebraic-data-types](algebraic-data-types/) | constructors, and why matching can be checked |
| [pattern-matching](pattern-matching/) | equations, order, exhaustiveness |
| [recursion-schemes](recursion-schemes/) | folds, unfolds, and why the direction matters |
| [list-functions](list-functions/) | the standard functions and the closure example |
| [higher-order](higher-order/) | currying, composition, partial application |
| [laziness](laziness/) | infinite structures that still terminate |

Lectures 1 to 5. No Haskell compiler is available on this machine, so the
semantics is reproduced in Python: constructors are tagged tuples, pattern
matching is a function over them, and laziness is a generator.

What survives that translation is what the block is about. The shape of a
data type determines the shape of every function over it, a fold is that
shape written once, and laziness is the reason the exam's infinite list of
solutions is a legitimate answer rather than a non-terminating program.
