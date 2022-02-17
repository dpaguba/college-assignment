# Equivalence transformations

The sheets ask for the transformation to NNF or CNF **step by step, naming the
law at each step**, which is why this module returns the sequence rather than
the answer. A function giving only the final formula answers the question and
teaches nothing about why the answer is right.

## The published derivation

`!(C <-> B) | !(!A | B)` reaches negation normal form in ten steps:

| step | formula | law |
|---|---|---|
| 0 | `!(C <-> B) \| !(!A \| B)` | |
| 1 | `!((C -> B) & (B -> C)) \| !(!A \| B)` | equivalence |
| 2 | `(!(C -> B) \| !(B -> C)) \| !(!A \| B)` | de morgan |
| 3 | `(!(!C \| B) \| !(B -> C)) \| !(!A \| B)` | implication |
| 5 | `((C & !B) \| !(B -> C)) \| !(!A \| B)` | double negation |
| 10 | `((C & !B) \| (B & !C)) \| (A & !B)` | double negation |

Every step is an equivalence, so every intermediate formula has exactly the
models of the original. That is checked rather than assumed: the model sets of
all eleven formulas are compared, not just the first and the last.

## Why CNF and not Tseitin

Distributing disjunction over conjunction can square the formula, and repeating
it makes the growth exponential. Tseitin's transformation avoids that by giving
up equivalence for equisatisfiability, and it lives in
[swk/verification/propositional-logic](../../../swk/verification/propositional-logic/).
The two are for different purposes: a solver wants Tseitin, an exercise asking
which formulas are equivalent wants this.

## Precedence

From loosest to tightest: `<->`, `->`, `|`, `&`, `!`, with implication right
associative. That last point is not cosmetic. `A -> B -> C` groups as
`A -> (B -> C)`, and the other grouping is not equivalent to it.
