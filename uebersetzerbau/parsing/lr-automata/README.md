# LR item automata

A bottom-up parser reduces the top of its stack when it matches a rule's right
side. Deciding **when** is the whole difficulty, and the answer is a finite
automaton over items: a rule with a dot marking how much has been seen, and a
state being a set of such items.

The four constructions differ only in how much lookahead an item carries.

## Measured, on three grammars

| grammar | LR(0) | LR(1) | LALR(1) | SLR conflicts | LR(1) conflicts |
|---|---|---|---|---|---|
| `S ::= S a S b \| c \| ε` (sheet 4) | 6 | **10** | **6** | 0 | 0 |
| expressions with priorities | 12 | 22 | 12 | 0 | 0 |
| odd palindromes `S ::= aSa \| bSb \| a \| b` | 8 | 20 | 8 | 4 | **4** |

The sheet 4 numbers are the published ones: the LR(1) automaton has 10 states,
LALR collapses it to 6, four pairs are merged, and no reduce-reduce conflict
appears. The merged pairs here are `{2,5} {3,6} {4,8} {7,9}` against the
solution's `q2+q5, q3+q6, q4+q7, q8+q9`: the same four merges, with the states
numbered in a different discovery order.

## Why LALR is what generators build

It has the state count of LR(0) and nearly the power of LR(1). The "nearly" is
precise: merging states with equal cores can create **reduce-reduce**
conflicts, because two states that each reduced unambiguously may disagree once
their lookaheads are pooled. It can never create a **shift-reduce** conflict,
since which symbols can be shifted depends only on the core.

In practice the merge is done during construction rather than after it, so the
canonical LR(1) automaton is never built.

## The odd palindrome grammar

`S ::= aSa | bSb | a | b` is not LR(1), and the conflict appears within two
transitions of the start state, which is what the sheet asks to show. After
reading one `a` the parser cannot tell whether it is the whole palindrome or
the opening symbol of a longer one, and no amount of lookahead at this point
helps: the decision depends on the length of the input, which is not bounded.

## SLR takes its lookahead from the wrong place

SLR reduces wherever the reduced nonterminal could **ever** be followed, rather
than where it could be followed in this state. That is coarser, and it is why a
grammar can be LR(1) and not SLR(1). Here the expression grammar is SLR(1) and
the palindrome grammar fails both, so the difference does not show up; it shows
up in grammars where the same nonterminal is used in two contexts with
different followers.
