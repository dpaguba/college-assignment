# First and Follow

`First(alpha)` is the set of terminals that can begin a string derived from
`alpha`, plus epsilon if `alpha` can vanish. `Follow(A)` is the set of
terminals that can appear immediately after `A`. Both are least fixed points,
and both exist for the same reason: a predictive parser has to choose a rule
from one lookahead symbol.

The lecture writes end of input as **epsilon** rather than `$`, and this module
follows that. The marker is the Greek letter and not the ASCII `e`, because `e`
is a perfectly ordinary terminal, and in the dangling-else grammar it means
`else`.

## The published sets

For `A ::= B c A a C | a`, `B ::= b B c | ε`, `C ::= c | B`:

| | First | Follow |
|---|---|---|
| A | a, b, c | a, ε |
| B | b, ε | a, c, ε |
| C | b, c, ε | a, ε |

matching the solution exactly, and reached in 4 rounds for both computations.

## Two readings of First differ while the iteration runs

The lecture computes First as the first symbols of the words derivable **so
far**, so a right side containing a nonterminal whose set is still empty
contributes nothing at all, even when it starts with a terminal: `B ::= b B c`
adds nothing in round 1 because `B` derives no word yet. The textbook reading
would add `b` immediately.

Both converge to the same sets. Reproducing the published round-by-round table
needs the lecture's reading, so that is what `first_iterations` implements.

One difference remains and is documented rather than hidden: the published
table has `First(A)` complete after round 2, which requires reading `First(B)`
as it is being updated within the same round. This module computes each round
from the previous one throughout, so `A` gains `b` in round 3 instead. The
final sets and the number of rounds are the same.

## Verified against the language

For both sheet grammars, the First set of every nonterminal contains the first
symbol of every word that nonterminal actually derives, checked against words
enumerated from the grammar up to length 5.
