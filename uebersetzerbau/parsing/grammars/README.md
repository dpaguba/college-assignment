# Grammars, parse trees and derivations

A grammar says which strings are programs; a parse tree says how one is built.
Everything after scanning hangs off the tree, so the question that matters is
not whether a word is in the language but whether its tree is unique.

## The published example

For the priority grammar `E ::= E+T | T`, `T ::= T*F | F`, `F ::= id | (E)` and
the expression `(id + id + id) * id`, the search finds exactly **one** parse
tree, and both derivations read off it have **15 sentential forms**, which is
the length the published solution prints.

The leftmost derivation begins `E → T → T*F → F*F → (E)*F` and the rightmost
begins `E → T → T*F → T*id → F*id`. They are the same tree traversed from
opposite ends, and the split matters: a top-down parser produces the leftmost
derivation as it runs, a bottom-up parser produces the rightmost one backwards.

## The enumeration has to be a chart

Enumerating parse trees by recursive descent does not terminate on
`E ::= E + T`: the search re-enters `E` at the same input position. Filling
spans shortest-first fixes it, because the recursive occurrence is always
looked up on a span that is already complete. Rules that stay within one span,
`E ::= T` or anything with nullable neighbours, are handled by iterating that
span to a fixed point.

This is a specification, not a parsing algorithm. It is what the LL and LR
parsers in the neighbouring folders are checked against.

## Epsilon needs a node

A nonterminal expanded by an empty rule would otherwise be indistinguishable
from a terminal leaf, and the yield of the tree would contain the
nonterminal's own name. It gets a single empty child instead, which is what
textbook drawings write an epsilon for.

## Ambiguity is a search, not a decision

Ambiguity is undecidable in general, so `find_ambiguity` proves ambiguity by
exhibiting a witness and proves nothing when it finds none.

| grammar | shortest witness |
|---|---|
| `E ::= E+E \| E*E \| id` | `id * id * id`, 5 symbols, 2 trees |
| palindromes `S ::= aSa \| bSb \| a \| b \| ε` | none up to length 6 |
| dangling else | `i b t i b t a e a`, 9 symbols, 2 trees |

The palindrome result is the computational half of the proof the sheet asks
for by induction: the grammar is unambiguous because the first character of a
palindrome determines the first rule.
