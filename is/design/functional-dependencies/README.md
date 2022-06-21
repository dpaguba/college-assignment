# Functional dependencies

The attribute closure is the whole toolkit. A dependency follows from a set
exactly when its right side lies in the closure of its left side, a set of
attributes is a key exactly when its closure is everything, and the minimal
cover is built by shrinking sides and dropping whatever the rest still
implies.

## Checking the closure against the axioms

`derive` applies reflexivity, augmentation and transitivity until nothing
changes, without using the closure at all. `armstrong_agrees` then compares
the two over every pair of attribute subsets. On `a → b`, `b → c`, `cd → e`
that is 32 × 32 = 1024 comparisons and all of them match, which is the
soundness and completeness of the closure algorithm demonstrated rather than
asserted.

The derivation is exponential and the closure is linear in the size of the
dependency set. That difference is the reason nobody computes the closure of
a dependency set directly.

On the same example the only key is `a d`, and the minimal cover drops the
added `a → c` because `a → b → c` already gives it.
