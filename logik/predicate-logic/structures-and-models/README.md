# Structures and models

A first-order formula is evaluated against a **structure**: a domain, a
relation for each relation symbol, a function for each function symbol, an
element for each constant. Free variables additionally need an assignment.

The definition is compositional and short, and everything interesting is in the
quantifier cases. The domain is part of the question, not part of the logic,
which is why the same formula holds in one structure and fails in another over
the same signature.

## The published database

Sheet 5 models a film site as `A = (A, F, N, L, S, c)`: films, users, likes,
similarity, and the featured film. On the example database:

| formula | holds | why |
|---|---|---|
| `F(c)` | yes | the featured item is a film |
| `forall x forall y (S(x,y) -> S(y,x))` | yes | similarity is symmetric |
| `forall x !S(x,x)` | yes | and irreflexive |
| `forall x (F(x) -> exists y (F(y) & S(x,y)))` | **no** | Forrest Gump is similar to nothing |
| the two-dissimilar-likes formula at Hannah | yes | she liked The Godfather and Forrest Gump |

The fourth row is the one the exercise is built around: the sentence says every
film has a similar film, and the database has a film that does not, so the
structure is not a model of it.

## A free variable has no truth value

Evaluating `F(x)` with no assignment for `x` raises rather than defaulting.
Returning false would be a guess, and the formula genuinely has no truth value
until `x` is given a value. The sheet makes the same distinction by writing
`(A, x -> Hannah) |= phi2` rather than `A |= phi2`.

## Equality

`Eq(y,z)` is interpreted as identity in the domain rather than as another
relation. Equality is not an ordinary symbol: a structure cannot choose what it
means, which is why formulas with equality are a distinct fragment.
