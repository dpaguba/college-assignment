# Shift-reduce parsing

Two actions and a stack of states. **Shift** pushes the next input symbol and
the state the automaton moves to. **Reduce** pops as many states as the rule
is long, then pushes the state reached from the exposed one by the rule's left
side. Everything grammar-specific lives in the table.

## The published run reproduced

Parsing `abacb` with `S ::= S a S b | c | ε` gives **11 configurations**, and
every one matches the solution: the same actions, the same stack depths
`1 2 3 4 5 2 3 4 4 5 2`, the same remaining input at each step.

| # | action |
|---|---|
| 1 | reduce `S ::= ε` |
| 2 | shift a |
| 3 | reduce `S ::= ε` |
| 4 | shift b |
| 5 | reduce `S ::= S a S b` |
| 6 | shift a |
| 7 | shift c |
| 8 | reduce `S ::= c` |
| 9 | shift b |
| 10 | reduce `S ::= S a S b` |
| 11 | accept |

The run starts with a reduction, which surprises people: the parser must
recognise the empty `S` before it can shift the first `a`, because the rule it
is heading for begins with `S`.

## Left recursion is not a problem here

`E ::= E + T` parses without any transformation, and a chain of four additions
parses fine. The recursive symbol is completed before it is needed, which is
exactly the opposite of the top-down situation. That is the practical argument
for bottom-up parsing, and the reason yacc-style tools accept grammars written
the way a language designer would write them.

## Reductions are a rightmost derivation backwards

The sequence of reductions, read in reverse, is the rightmost derivation of the
input: for `id + id * id` there are as many reductions as the derivation has
steps. The tree built by pushing subtrees alongside the states is identical to
the one the reference parser produces.

## A conflict is a build-time error

`E ::= E + E | id` raises rather than parsing badly. The table cannot be built,
which is the accurate report: the grammar is ambiguous, and no deterministic
parser of this class exists for it. Real generators resolve such conflicts by
rule and warn, which is convenient and hides exactly this fact.

## Verified

Acceptance matches the grammar's language on all words up to length 5 over the
sheet grammar's alphabet, and the parse tree matches the reference chart parser
on the expression grammar.
