# From a regular expression to a DFA

Three steps, all mechanical: rewrite the extended operators away, build an
epsilon-NFA by Thompson's patterns, determinise by the subset construction.
That is why nobody writes a scanner by hand.

## The rewriting is a definition, not an approximation

The lecture requires `a+` to become `a.a*` and `a?` to become `(a|)` before
Thompson's construction is applied, because the construction has patterns for
three operators and not five. `(a+|b).c*` expands to `(a.a*|b).c*`, which is
exactly the form the published solution works from.

## Sizes

| expression | NFA states | DFA states | minimised |
|---|---|---|---|
| `(a+\|b).c*` | 14 | 5 | **3** |
| `(a\|b)*abb` | 14 | 5 | 4 |
| `(aa\|bb)*` | 12 | 5 | 3 |
| `10\|1(0\|1)*10` | 20 | 6 | 4 |

The 3 states for the lecture example are the ones the solution arrives at by
collapsing the two upper and the two lower states of the subset automaton.

## The subset construction really is exponential

`(a|b)*a(a|b)^k` forces the automaton to remember the last `k+1` characters:

| k | NFA states | DFA states | `2^(k+1)` |
|---|---|---|---|
| 1 | 16 | 5 | 4 |
| 3 | 28 | 17 | 16 |
| 5 | 40 | 65 | 64 |
| 7 | 52 | 257 | 256 |
| 9 | 64 | **1025** | 1024 |

Linear in the expression, exponential in the automaton. It is also why the
construction is written as a worklist over reachable subsets: enumerating the
whole power set would build states nothing can reach.

## Checked against the published solutions

Sheet 1 gives three regular expressions and, unusually, also says why two
plausible alternatives are wrong. Both claims are reproduced here:

- `1(0|1)*10` is correct but incomplete: it rejects `10`, the number 2, which
  `10|1(0|1)*10` accepts. Over all binary words up to length 10 the full
  expression accepts exactly the even numbers without leading zeros that are
  not divisible by 4.
- `(b|abb?)*` is complete but incorrect: it accepts `abbb`, which violates the
  rule. `b*(abb?)*` rejects it, and agrees with the rule checked literally on
  every word over `{a,b}` up to length 8.

The third expression, `(aa|bb)*(a|b|(ab|ba)(a|b)*)`, accepts exactly the
complement of `(aa|bb)*` on all 2046 words up to length 10.

## Relationship to GTI

Thompson's construction, the subset construction and minimisation are proved
in [gti/regular-languages](../../../gti/regular-languages/). What is added
here is the lecture's numbering convention (start state 0, ascending in the
direction of the arrows), the partial transition function a scanner needs, and
`longest_match`, which keeps running past an accepting state because a longer
token may still follow.
