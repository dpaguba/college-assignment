# Categories

| Topic | |
|---|---|
| [categories](categories/) | objects, arrows, two laws |
| [variance](variance/) | which way a map may travel |
| [natural-transformations](natural-transformations/) | maps that ignore the values |

Lecture 12, and the block that explains the earlier ones. Haskell's `Functor`
is a functor on the category of types and functions, its laws are the functor
laws, and a polymorphic function between two functors is natural exactly when
it cannot inspect the values it moves.

Everything here is checked by enumeration on small examples, including the
failures: a category missing one composite, a map that forgets composition,
and a transformation that filters on the values. Each of them breaks exactly
one law, which is the useful way to read a definition with several clauses.
