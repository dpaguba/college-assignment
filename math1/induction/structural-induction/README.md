# Structural induction

A claim about every structure is proved by showing it for the base cases and
for each way of building a larger structure from smaller ones. Enumerating
the structures does not replace the proof, and it does the one thing the
proof cannot: it produces a counterexample when the claim is false.

The claim checked here is that a binary tree has one more leaf than it has
branching nodes. It holds for all 26 trees of depth three and all 677 of
depth four, which is not a proof and is a strong reason to look for one.

## What enumeration is for

The useful direction is refutation. A claim like "every tree of depth three
has fewer than three leaves" is checked and comes back with the tree that
breaks it, immediately and with no argument required. Most failed proofs
begin as claims of exactly that kind, and finding the counterexample first
saves the proof attempt.
