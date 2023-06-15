# Chomsky normal form

Every rule is `A -> B C` or `A -> a`, plus `S -> eps` if the empty word is in
the language.

The point is [CYK](../cyk/): with rules of that shape a parser fills a table
over substrings and never has to guess how far a rule reaches.

## The five steps of the course

| Step | Does |
|---|---|
| CNF1 | remove useless variables, generating before reachable |
| CNF2 | replace terminals in right-hand sides by fresh variables |
| CNF3 | shorten right-hand sides to length two |
| CNF4 | remove epsilon rules |
| CNF5 | remove unit rules |

CNF2 replaces terminals **everywhere**, including in a rule that is a single
terminal, so `B -> b` becomes the unit rule `B -> Wb` and CNF5 turns it back
into `B -> b`. That looks like a detour and it is what the course does, because
it makes CNF3 a pure shortening step with no terminals to think about.

## Verified against the sheet, all three parts

Sheet 5 publishes the input and output of each step:

- **CNF1**: generating `{S,A,B,C,D,G}`, reachable `{S,A,B,D}`, and `G1` matches
- **CNF2 and CNF3**: `G2` matches rule for rule; `G3` matches up to the names
  of the four fresh variables, which the solution calls `U1, V1, V2, V3` and
  this module calls `X1..X4`
- **CNF4 and CNF5**: nullable set `{A, B, C}`, and both `G4` and `G5` match
  exactly

## One repair the five steps do not cover

Unit removal can leave a pair containing a terminal, such as `A -> Wb Wc`
collapsing into `A -> b Wc`. `_repair_terminals` puts those back through a
terminal variable, which is CNF2 applied once more where it is needed.
