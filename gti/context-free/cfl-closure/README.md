# Closure properties of context-free languages

| Operation | Closed |
|---|---|
| union, concatenation, star | yes, by a new start rule |
| intersection with a **regular** language | yes, by the triple construction |
| intersection with a context-free language | **no** |
| complement | **no** |

That asymmetry is the main structural difference from the regular level, where
everything was closed.

## The counterexample, computed

`a^i b^i c^j` and `a^i b^j c^j` are both context-free: each keeps one count,
which is all a stack can do. Their intersection is

```
{'', 'abc', 'aabbcc'}   up to length 6
```

which is `a^n b^n c^n`, and the [pumping lemma](../cfl-pumping-lemma/) shows it
is not context-free. Non-closure under complement follows: closure under
complement and union would give closure under intersection by De Morgan.

## Why intersection with a regular language does hold

The triple construction threads the automaton's states through the grammar's
rules. A finite automaton contributes **finitely many** states to thread; a
second pushdown automaton would contribute a second stack, and no machine of
this class has two.

That is also why the construction is the standard tool for proving a language
non-context-free: intersect with something regular until what is left is a
known bad case.

## One small design choice

`star` uses `S -> A S | eps` rather than `S -> S S | eps`. Both are correct;
the second makes every word ambiguous for no reason at all.
