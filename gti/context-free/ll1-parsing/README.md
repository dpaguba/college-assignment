# LL(1) parsing

Left to right, leftmost derivation, one symbol of lookahead. The parser must
choose the right rule from the next input symbol alone, and two sets decide
whether it can.

```
FIRST(alpha)  terminals that can start a string derived from alpha, plus eps
FOLLOW(A)     terminals that can appear directly after A
```

| Conflict | Means |
|---|---|
| first/first | two rules for A whose right sides can start with the same terminal |
| first/follow | A can vanish, and FIRST(A) meets FOLLOW(A), so "expand" and "skip" look alike |

## Verified against sheet 7

The sheet gives three grammars and asks for a verdict with the sets that
justify it. All three come out:

| Grammar | Verdict | Reason |
|---|---|---|
| G1 | not LL(1) | first/follow conflict |
| G2 | not LL(1) | first/first conflict on A, shared `{b}` |
| G3 | **is** LL(1) | no conflicts |

And every published set matches exactly, including the FIRST sets of the
right-hand sides:

```
FIRST(S) = {a,b,c,d}   FOLLOW(S) = {}
FIRST(A) = {a,eps}     FOLLOW(A) = {b,c,d}
FIRST(B) = {b,eps}     FOLLOW(B) = {a,c,d}
FIRST(C) = {a,b,c,eps} FOLLOW(C) = {}
```

## One convention worth naming

The course computes FOLLOW **without an end marker**, which is why `FOLLOW(S)`
is empty for a start symbol that never occurs inside a rule. Adding the marker
is the other common convention and changes nothing about which grammars are
LL(1); the sets are just printed differently. The parameter is there and
defaults to the course's choice.

## The table is the same test

An entry of the parse table holding two rules **is** a conflict, so building
the table and listing conflicts are the same computation seen from the parser's
side and from the grammar's.
