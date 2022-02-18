# Propositional resolution

One rule: two clauses with complementary literals resolve to their union minus
that pair. Deriving the empty clause proves unsatisfiability, and the sequence
of steps is the proof.

Resolution is **refutation complete**: it derives the empty clause from every
unsatisfiable clause set and from no satisfiable one. It is not complete for
deriving arbitrary consequences, which is why every use starts by negating what
is to be proved.

## Checked against truth tables

Over every subset of ten representative clauses up to size 3, resolution finds
a refutation exactly when the truth table says the set is unsatisfiable. Both
directions matter: a prover that refutes too much is unsound, one that refutes
too little is incomplete.

## The published entailment

Sheet 2 asks to show that the four holiday conditions entail "if they visit the
wildlife park then they visit the computing museum but not the art museum". The
refutation of the conditions together with the negated conclusion succeeds, and
without the conditions it does not.

The proof found by saturation takes **32 resolution steps** and produces 40
clauses. The published proof takes a handful. That gap is the whole reason
practical provers exist: saturation resolves every pair that can be resolved,
while a person resolves the pairs that lead somewhere.

## Two cheap restrictions

Tautological resolvents, containing a literal and its complement, are
discarded: they are satisfied by every assignment, so they cannot contribute to
a refutation, and keeping them makes the saturation much larger. Duplicate
clauses are dropped for the same reason.

Everything beyond that, ordering, subsumption, unit preference, is what
separates this from a usable prover, and is why DPLL and CDCL in
[swk/verification](../../../swk/verification/) are different machines rather
than optimisations of this one.
