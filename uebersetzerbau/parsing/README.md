# Parsing

From a token sequence to a tree. Two families, split by which derivation they
build.

| Topic | |
|---|---|
| [grammars](grammars/) | trees, derivations, ambiguity, and the reference parser everything else is checked against |
| [first-follow](first-follow/) | the two set computations every predictive method needs |
| [ll1-parser](ll1-parser/) | table-driven top-down parsing |
| [grammar-transformations](grammar-transformations/) | making a grammar fit a top-down parser |
| [lr-automata](lr-automata/) | LR(0), SLR(1), LR(1), LALR(1) item automata |
| [shift-reduce-parser](shift-reduce-parser/) | the driver that runs an LR table |

## The one distinction

A top-down parser builds a leftmost derivation forwards and must decide which
rule to use **before** seeing what the rule produces. A bottom-up parser builds
a rightmost derivation backwards and decides **after**. Every asymmetry between
the two follows from that: left recursion is fatal to one and irrelevant to the
other, and the tables of the second are larger for the same reason they are
more powerful.

## Checked against the published solutions

Sheets 2, 3 and 4 come with full solutions, and the modules reproduce them:
the parse trees and both derivations for `(id+id+id)*id`, both LL(1) tables,
both First and Follow computations including the round-by-round trace, the
LR(1) automaton with 10 states collapsing to 6 under LALR, and the 11-step
shift-reduce run on `abacb`.
