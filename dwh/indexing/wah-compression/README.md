# WAH compression

Cut the bitmap into groups of one bit less than a word. Store a group
literally, or replace a run of uniform groups by a fill word that counts
them.

The fifth exercise sheet's sequence is 1 zero, 20 ones, 3 zeros, 79 ones and
21 zeros, 124 bits at a word length of 32:

| word | kind | content |
|---|---|---|
| 1 | literal | the first 31 bits |
| 2 | fill | 2 groups of ones |
| 3 | literal | the last 31 bits |

Three words, 96 bits against 124, and the decoding returns the original
exactly.

## Why the alignment matters

The groups line up, so a conjunction can be computed on the encoded form
directly: a fill of zeros meets anything and stays zero, a fill of ones
passes the other side through, and only two literals need a bitwise
operation. The module computes the conjunction that way and checks it against
the decoded answer, which is what the exercise asks to demonstrate.

Alternating bits compress to nothing at all, which the module also checks. A
compression that assumes runs has no runs to find in a bitmap with none.
