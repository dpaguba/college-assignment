# Modal satisfiability

Modal logic has the **finite model property**: a satisfiable formula has a
model whose size is bounded in the formula's length. That is what makes
satisfiability decidable, and it is why searching small structures is a
decision procedure rather than a heuristic, as long as the bound is respected.

| formula | result |
|---|---|
| `<>A & <>!A` | satisfiable, needs two successors |
| `A & !A` | unsatisfiable |
| `[]A & <>!A` | unsatisfiable |
| `[](A & !A)` | satisfiable, **only in a world with no successors** |

The last row is the one worth pausing on. `[]` of a contradiction is satisfied
by a dead end, and the model the search returns has exactly that shape.

## Validity is the dual

`valid(phi)` asks whether `!phi` is unsatisfiable. The K axiom
`[](A -> B) -> ([]A -> []B)` comes out valid; `[]A -> A` and `[]A -> <>A` do
not, and their counterexamples are one world with no successors.

## Why this is a teaching procedure

Enumerating structures is exponential in both the number of worlds and the
number of atoms: two worlds and two atoms already give 4096 structures. A real
decision procedure is a tableau calculus, which builds only the worlds the
formula forces to exist. The enumeration is here because it is obviously
correct, and it states the bound rather than pretending to decide.
