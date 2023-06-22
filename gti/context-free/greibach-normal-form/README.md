# Greibach normal form

Every rule is `A -> a alpha`: one terminal, then variables only.

The consequence is what matters. Each derivation step produces exactly one
terminal, so a word of length n takes exactly n steps, and a top-down parser
can read the input without ever looping, because no rule consumes nothing.

## Left recursion is the obstacle

`A -> A b` can never start with a terminal. The fix turns it right-recursive:

```
A -> A b | c        becomes        A -> c | c A'
                                   A' -> b | b A'
```

That is the same transformation a recursive descent parser needs, which is why
it shows up again in [LL(1)](../ll1-parsing/) preparation. Indirect recursion,
where A reaches itself through other variables, is removed by the ordered
substitution in the main conversion.

## The blow-up

Substitution multiplies rules. `S -> (S) | SS | a` goes from three rules to
fifteen, and larger grammars do much worse. Greibach normal form is a
theoretical tool, and this is the reason no compiler uses it.

## Verified

Three grammars converted, each checked twice: the shape of every rule, and the
language up to length 4 against the original through
[CYK](../cyk/). All three preserved the language exactly.
