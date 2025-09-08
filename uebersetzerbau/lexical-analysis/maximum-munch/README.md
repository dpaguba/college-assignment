# Maximum munch

Two rules decide every tokenisation:

- **longest match**: among all specifications matching a prefix, the one with
  the longest prefix wins, regardless of the order they were written in
- **priority**: among matches of equal length, the one listed first wins

Neither is arbitrary. Longest match is why `iffa` is one identifier rather than
the keyword `if` followed by `fa`. Priority is why `if` is the keyword and not
an identifier, since both match exactly two characters.

## The published example, step by step

Sheet 1 task 3 gives `T1 = 010*(1|0)`, `T2 = 0101?0?`, `T3 = 0?11?(0|1)` and
the input `011001011001001`. `trace` reports the whole decision:

| position | how far each rule matches | winner |
|---|---|---|
| 0 | T1: 3, T3: 4 | T3 `0110` |
| 4 | T1: 4, T2: 4, T3: 3 | **T1 `0101`, priority beats T2** |
| 8 | T3: 2 | T3 `10` |
| 10 | T1: 5, T2: 4, T3: 3 | T1 `01001` |

which is the published answer `T3(0110), T1(0101), T3(10), T1(01001)`,
including the remark that the second token is where priority decides.

## Why a zero-length match is not a match

A rule whose language contains the empty word matches at every position with
length 0. Accepting that would make the scanner emit an endless stream of empty
tokens without ever advancing, which is the classic way a hand-written lexer
hangs. `_longest` requires a strictly positive length, so `a*` against the
input `b` raises a scan error instead.

## Errors carry a position

The only useful part of a lexical error message is which character could not
start any token. `ScanError` carries it, and the scanner reports position 2 for
input `aab` against the single rule `a`.

## One automaton per rule

This module runs every rule's automaton at every position, which makes the
priority rule trivial to state and is quadratic in the number of rules. The
form a real generator uses, one merged automaton, is in
[lexer-generator](../lexer-generator/).
