# Regular expressions

Syntax, semantics, and matching without building an automaton.

The core has five cases: empty set, epsilon, a symbol, union, concatenation and
star. Everything else, `+` and `?` included, is an abbreviation. Keeping the
core that small is what makes the proofs short: an induction over the syntax
has five cases and no more.

## Matching by derivatives

`derivative(a)` is what remains of an expression after reading the symbol `a`,
defined so that

```
w in L(derivative(r, a))   exactly when   a + w in L(r)
```

Matching is then: read the word symbol by symbol, replacing the expression by
its derivative, and ask at the end whether what is left contains the empty
word. Brzozowski published it in 1964 and it is still the shortest correct
matcher there is, in five recursive cases and no automaton.

The simplification in `union`, `concat` and `star` is not cosmetic. Derivatives
grow the expression on every symbol, and without collapsing empty sets and
duplicates the terms double in size per step.

## One notation decision, and the bug it prevented

Some textbooks write the empty set as `0`. Doing that here silently turned the
pattern `(0|1)+` into `1+`, because the digit was parsed as the empty set, and
the lexer in [applications](../applications/) then failed on the input `10`
with no error from the regex layer at all.

So the empty set is `empty` or the character for it, epsilon is `eps` or the
Greek letter, digits are ordinary symbols, and a backslash escapes the next
character so `\+` is a plus sign rather than an operator.

## Comparing two expressions

`equivalent_up_to` compares them on every word up to a length and returns the
first disagreement. It is a **test**: agreement up to length k proves nothing
about longer words. The real decision procedure goes through automata and is in
[decision-algorithms](../decision-algorithms/).
