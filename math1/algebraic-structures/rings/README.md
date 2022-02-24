# Rings

Two operations, tied by distribution. An abelian group under addition, a
monoid under multiplication, and nothing said about inverses for
multiplication, which is where all the variety comes from.

The residues modulo n are the running example, because n decides everything:

| | Z/7 | Z/12 |
|---|---|---|
| units | all six non-zero | 1, 5, 7, 11 |
| zero divisors | none | 2, 3, 4, 6, 8, 9, 10 |
| a field | yes | no |

An element is a unit exactly when it is coprime to the modulus, and a zero
divisor exactly when it is not and not zero, so the two conditions are
complementary here. That is a property of the residues rather than of rings
in general: in the ring of integers, 2 is neither a unit nor a zero divisor.

Polynomials over the two-element field, truncated at a degree, give a second
example whose multiplication is not the obvious one, and the same law checks
apply to it unchanged, which is the point of stating the axioms rather than
the examples.
