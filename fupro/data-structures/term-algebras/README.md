# Term algebras

A term built from constructors carries no meaning. An algebra assigns a value
to each constructor, and folding the term with that algebra gives it one:

| algebra | `Add (Lit 2) (Lit 3)` |
|---|---|
| value | 5 |
| size | 3 |
| text | `(2 + 3)` |

Same term, same traversal, three answers. That separation is the reason a
compiler can evaluate, measure and print an expression with one walk over the
syntax tree and three sets of cases.

The formal statement is that the term algebra is initial: from it there is
exactly one homomorphism into any other algebra. Uniqueness is the useful
half, since it says a fold is determined by its algebra and by nothing else,
so two definitions that agree on the constructors agree everywhere.
