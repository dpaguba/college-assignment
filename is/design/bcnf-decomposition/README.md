# Decomposition into Boyce-Codd normal form

Find a dependency `X → Y` whose left side is not a superkey, split the schema
into `X⁺` and `X ∪ (R − X⁺)`, and repeat. The result is always in Boyce-Codd
normal form and always lossless, and the module checks both.

## The tableau test

Losslessness is checked with the tableau method: one row per fragment,
distinguished symbols where the fragment has the attribute, then the
dependencies are applied until nothing changes. A row of only distinguished
symbols means the join reconstructs the original.

The test was verified against the thing it stands for. On the schema `a b c`
with `a → b`, `b → c` and the instance `(1,1,1), (2,1,1), (3,2,2)` the
tableau says lossless and the actual join of the projections returns exactly
the three rows. On `a b` and `a c` with only `b → c` the tableau says lossy
and the join of the instance `(1,1,1), (1,2,2)` returns four rows instead of
two.

## What it cannot promise

On student, subject, teacher the decomposition produces `{subject, teacher}`
and `{student, teacher}`, and `{student, subject} → teacher` is no longer
checkable inside either fragment. Boyce-Codd normal form and dependency
preservation cannot always be had at once; that is the reason the third
normal form is still used.
