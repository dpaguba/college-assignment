# LL(1) parsing

Left to right, **L**eftmost derivation, **1** symbol of lookahead. A stack of
grammar symbols and a table saying which rule to apply for a nonterminal on top
and a terminal ahead.

A rule `A ::= alpha` goes into the table under every terminal that can begin
`alpha`, and if `alpha` can vanish, under everything in `Follow(A)`, because
choosing a vanishing rule is really a decision about what comes next.

## Both published tables reproduced

For `A ::= B c A a C | a`, `B ::= b B c | ε`, `C ::= c | B`, 11 cells:

| | a | b | c | ε |
|---|---|---|---|---|
| A | a | B c A a C | B c A a C | |
| B | ε | b B c | ε | ε |
| C | B | B | c | B |

The C row is the interesting one: `C ::= B` is entered wherever `B` can start,
and because `B` is nullable, also wherever `C` can be followed.

The second grammar's table has 10 cells and no conflicts, and the parser's run
on `aabcbrbr` reproduces the published protocol step for step: 18 actions, the
same stack contents, the same shrinking input.

## Conflicts are a statement about the grammar

| grammar | conflicts |
|---|---|
| `E ::= E + T \| T`, left recursive | 4 |
| the same after removing left recursion | 0 |
| `S ::= i E t S \| i E t S e S \| a`, common prefix | on `S` at lookahead `i` |

A conflict does not mean the parser is broken. It means one lookahead symbol
genuinely does not determine the rule, and the fix is either to transform the
grammar, as in [grammar-transformations](../grammar-transformations/), or to
use a stronger method.

## The tree comes for free

A predictive parser produces a leftmost derivation, and a leftmost derivation
is a tree built top down and left to right. Keeping a parallel stack of tree
nodes turns the recogniser into a parser at no extra cost, and the tree it
produces is identical to the reference parser's.

Acceptance was checked exhaustively: on all words up to length 6 over the
second sheet grammar's alphabet, the parser accepts exactly the words the
grammar derives.
