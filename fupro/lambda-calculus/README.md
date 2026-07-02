# Lambda calculus

| Topic | |
|---|---|
| [syntax-and-substitution](syntax-and-substitution/) | three forms, and the renaming that makes substitution safe |
| [reduction-strategies](reduction-strategies/) | which redex first, and what that decides |
| [church-encodings](church-encodings/) | the lecture's own terms, reduced and read back |
| [fixed-points](fixed-points/) | recursion without names |

Lectures 9 and 11. The interpreter here is the oracle for the whole block:
every term of the lecture's `terms.txt` is parsed, reduced and converted back
into a Python value, so `ADD TWO THREE` being 5 is a computation rather than
a claim.

Two results are worth carrying forward. Call by value diverges on a term
whose discarded argument has no normal form, which is the argument for lazy
evaluation stated as a program. And the parity predicate from the exam
computes nothing at all if the two arguments of the numeral are swapped,
which is the argument for stating a convention before using it.
