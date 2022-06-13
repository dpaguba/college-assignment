# Rice's theorem

> Every non-trivial property of the **language** of a machine is undecidable.

Non-trivial means some machine has it and some machine does not. That is the
entire hypothesis, and the conclusion covers emptiness, finiteness, regularity,
containing a given word, and equality with another language, all at once.

The proof is one reduction: from `(M, w)`, build a machine that behaves like a
witness for the property when M accepts w and like a machine lacking it
otherwise. That construction is the one in [reductions](../reductions/).

## The boundary is the exam question

| Property | Kind | Decidable |
|---|---|---|
| accepts the empty word | semantic | no, by Rice |
| language is empty | semantic | no, by Rice |
| contains a word of length >= 2 | semantic | no, by Rice |
| has at most five states | **syntactic** | yes, count them |
| halts within 20 steps | **syntactic** | yes, run it |

Rice is about what a machine **computes**, not about how it is written. The
classifier here tests both conditions on a sample and names which of the three
cases applies.

## The sample has to be able to fail

The first version of the sample machines could not tell syntactic from
semantic: the two machines with the same language both had fewer than five
states, so the state-count property passed as semantic and was reported
undecidable.

A sample without a pair that a syntactic property can separate makes the test
toothless. The fixed sample has two machines with identical languages and two
versus seven states, and the classifier now reports the state count as
syntactic, as it should.
