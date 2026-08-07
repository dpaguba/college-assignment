# Grammar transformations

Left recursion and common prefixes are properties of the **grammar**, not of
the language, and both block a top-down parser. Both can be removed
mechanically. Ambiguity cannot.

## Removing left recursion

    A ::= A alpha | beta      becomes      A ::= beta A'
                                           A' ::= alpha A' | ε

Paull's algorithm substitutes earlier nonterminals first, which turns indirect
recursion into direct recursion, then removes the direct case.

On the expression grammar:

| | before | after |
|---|---|---|
| rules | 6 | 9 |
| nonterminals | 3 | 5 |
| LL(1) conflicts | **4** | **0** |

and the language is unchanged, verified on every word up to length 5.

The result is

    E  ::= T E2
    E2 ::= + T E2 | ε
    T  ::= id T2 | ( E ) T2
    T2 ::= * F T2 | ε
    F  ::= id | ( E )

The cost is not visible in that table: the transformation destroys the shape of
the parse tree. `E2` collects the tail of what used to be a left-recursive
list, so a compiler that wanted left associativity has to rebuild it while
walking the tree.

Indirect recursion is detected through the transitive closure of "can appear
leftmost", which has to look past nullable symbols: in `S ::= A a`,
`A ::= A c | S d | ε`, both `S` and `A` reach themselves.

## Left factoring

    A ::= alpha beta | alpha gamma     becomes     A ::= alpha A'
                                                   A' ::= beta | gamma

The parser then decides after reading `alpha` instead of before, which is
exactly the information it was missing.

## What factoring cannot fix

The dangling-else grammar factors to

    S  ::= a | i E t S S2
    S2 ::= ε | e S

and still has one LL(1) conflict, now on `S2` at lookahead `e`: after an inner
`if` the parser cannot tell whether the `else` belongs to it or to an outer
one. It cannot, because the grammar is **ambiguous**: `i b t i b t a e a` has
two parse trees before factoring and two after.

Factoring moved the conflict and shrank it to one cell. Removing it needs
either a different grammar or a resolution rule, which is what real parser
generators do when they prefer shift over reduce.
