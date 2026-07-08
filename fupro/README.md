# Funktionale Programmierung

Twenty-three modules in six blocks, covering the fourteen lectures. There is
no Haskell compiler on this machine, so the semantics is reproduced in
Python: constructors are tagged tuples, laziness is a generator, and the
lambda calculus has an interpreter.

| Block | |
|---|---|
| [haskell-core](haskell-core/) | data types, matching, folds, lists, currying, laziness |
| [type-classes](type-classes/) | classes, Functor, Applicative, Monad, and their laws |
| [data-structures](data-structures/) | the exam's tree and binary numbers, term algebras |
| [lambda-calculus](lambda-calculus/) | syntax, reduction, Church encodings, fixed points |
| [type-systems](type-systems/) | the simply typed calculus, unification, inference |
| [categories](categories/) | objects and arrows, variance, naturality |

## The course's own terms, reproduced

The lecture ships `terms.txt` with twenty-one lambda terms. All of them parse,
reduce and read back as values: `ADD TWO THREE` is 5, `MULT TWO THREE` is 6,
`LENGTH NEZ` is 3 and `LENGTH (CONCAT NEZ NEZ)` is 6.

## The 2024 exam, reproduced

| Task | |
|---|---|
| 1, trees | `hoehe`, `preorder`, and the Functor instance |
| 2, list monad | the productive list of solutions, `mapM`, `tryMap` |
| 3, binary numbers | `foldB`, `shift`, `rlz`, and the `Eq` instance |
| 4, State monad | `clear`, `pushN`, `popN` on a stack |
| 5, lambda calculus | the reduction to `\x.\a.(x a)`, and the type `(a -> b) -> a` |
| 6, Church encodings | `even`, and the encoding of `Bin` |

## Three results worth keeping

**The obvious fold over the exam's binary numbers is wrong.** The traversal
starts at the marker, which is the least significant end, so the algebra that
doubles and adds computes the value of the reversed bit string: 11 for the
term of 13. Nine of the sixteen numbers below sixteen come out wrong, and the
seven that agree are the palindromes, which is how such an implementation
passes a careless test.

**A Church predicate written for the wrong argument order computes nothing.**
The lecture's numerals apply their first argument n times to the second; the
exam writes them the other way round, as a fold. The parity predicate written
for one convention returns false for every input under the other, including
zero.

**Type variables and type constants must be different things.** With both
represented as strings, an environment mentioning a base type `a` has that
`a` unified with an arrow type, and the exam's perfectly typable term comes
back as an infinite type.

## Verification

The lambda interpreter is the oracle for everything the calculus touches: a
term is not asserted to reduce to something, it is reduced. The type
inference is checked by comparing its principal types with the ones the
lecture derives, and by requiring that a specific type is rejected as
principal where a general one exists. The type class laws are checked by
running both sides on samples, with a deliberately broken instance at each
level to show the check has teeth.
