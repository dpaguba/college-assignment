# A lexer generator

What lex and flex do: merge every rule into one NFA with a fresh start state
and epsilon edges into each rule's fragment, determinise once, and label each
accepting state with the highest-priority rule whose accepting state its subset
contains.

The output is a table and a driver loop. The regular expressions have
disappeared entirely by run time.

## The merge pays off

For a six-rule specification with keywords, identifiers, numbers, an operator
and whitespace:

| approach | states |
|---|---|
| one automaton per rule | 43 in total |
| merged | **36**, 35 of them accepting, 298 transitions |

The saving is small here and grows with the number of rules that share
prefixes, which in a real language is most of them: every keyword shares its
prefix with the identifier rule.

## Priority lives in the labels

A DFA state whose subset contains the accepting states of several rules is
labelled with the first rule listed. With `IF` before `ID`, the state reached
by reading `if` is labelled `IF`; with the rules in the other order, the same
state is labelled `ID`. Nothing else in the generator changes.

## The backup rule

The driver keeps reading past an accepting state, because a longer match may
follow, and returns to the last accepting position when it gets stuck. Without
that, input `abab` against rules `ab` and `abcd` would fail at the third
character rather than yielding two tokens.

That single mechanism is why a generated scanner needs to remember one state
and one position rather than backtracking through the input.

## Verified

Against the per-rule scanner in [maximum-munch](../maximum-munch/): identical
tokenisation, including identical failures, on **all 2046** binary words up to
length 10 for the sheet specification, and on 200 random programs built from a
six-rule language specification.
