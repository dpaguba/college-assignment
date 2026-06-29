# Data structures

| Topic | |
|---|---|
| [trees](trees/) | the exam's binary tree and its functor instance |
| [binary-numbers](binary-numbers/) | the exam's `Bin`, and the fold that reads it backwards |
| [term-algebras](term-algebras/) | one term, three meanings |
| [homomorphisms](homomorphisms/) | maps that respect a structure |

Lecture 8 and two exam tasks. The block ends where the theory starts: a fold
is a homomorphism out of the term algebra, and the term algebra is initial,
so the fold is unique.

The concrete result is the binary numbers. The fold the exam asks for
traverses from the marker outwards, so the algebra that simply doubles
computes the value of the reversed bit string: 11 instead of 13, and nine of
the sixteen numbers below sixteen come out wrong. The correct fold carries the
place value with it, and the difference is invisible on palindromes, which is
how a wrong implementation survives testing.
