# Attribute grammars

A context-free grammar cannot say that two parts of a program agree: that a
variable is declared before use, that argument counts match, that a word has as
many `b`s as `a`s. Attributes add exactly that without leaving the
syntax-directed framework.

## The published example

`{a^n b^n a^n}` is not context free. The sheet's grammar
`S ::= A B A`, `A ::= ε | a A`, `B ::= b | B b` generates the larger language
`{a^n b^m a^k}`, and a synthesized counter plus one comparison cuts it down:

    S ::= A1 B A2    S.ok = (A1.cnt == B.cnt and A2.cnt == B.cnt)
    A ::= ε          A.cnt = 0
    A ::= a A1       A.cnt = A1.cnt + 1
    B ::= b          B.cnt = 1
    B ::= B1 b       B.cnt = B1.cnt + 1

On `aabbaa` the three counters come out 2, 2, 2 and `ok` is true. Of the **56**
words the grammar generates up to length 6, the attributes accept exactly
**2**: `aba` and `aabbaa`, which are `a^1 b^1 a^1` and `a^2 b^2 a^2`.

## Synthesized and inherited

Synthesized attributes flow upwards from the children, inherited ones downwards
from the parent and the left siblings. The distinction decides when they can be
computed:

| class | condition | evaluated during |
|---|---|---|
| S-attributed | only synthesized | a bottom-up parse, on the parser stack |
| L-attributed | inherited depend on the parent and on left siblings only | a top-down parse, while descending |

That is what yacc's `$$` and `$1` are: an S-attributed evaluator built into the
shift-reduce driver, which is why they only ever look downwards.

The published grammar is both, so it could be evaluated by either parser with
no tree at all.

## The dependency check is run, not read

`dependencies` runs each semantic rule once against recording dictionaries that
return zero, and observes which attributes it reads. That gives the dependency
graph without parsing the rule's source. A rule with a branch reveals only the
side it took, so this reports a dependency set rather than proving one, which
is enough to catch the case that matters: an inherited attribute of a child
reading a child to its right is not L-attributed.

## Evaluation order is computed, not assumed

The evaluator schedules by dependency and reports a cycle when no order exists.
On `aabbaa` it computes the innermost counters first and `ok` last, in nine
steps. A general attribute grammar needs this; the two restricted classes above
exist precisely so that a compiler never has to build the graph.
