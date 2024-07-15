# Applications

What the theory is actually for: searching and tokenising.

## Searching

`search_automaton` builds a DFA for `S* p S*` and scans a text in one pass with
no backtracking. That is the property separating automaton matching from the
backtracking regex engines that can be driven to exponential time by a pattern
like `(a+)+b` on a string of `a`s.

`word_count_automaton` puts several patterns into **one** automaton, so
scanning for twenty words costs what scanning for one costs. Three words
`cat, car, cart` become six states, and that idea scaled up is Aho-Corasick.

## Tokenising

A lexer is one automaton per token kind and two conventions:

- **longest match**: keep reading while any automaton could still accept, and
  report the longest prefix that some automaton did accept. This is why `ifs`
  is one identifier rather than the keyword `if` followed by `s`.
- **priority**: when several kinds match the same longest prefix, the one
  declared first wins, which is how keywords beat identifiers.

Neither convention follows from the theory. The theory says only that each
token kind is a regular language; the rest is what a scanner generator decides
for you.

```
'while abc<10' -> KEYWORD('while')@0 IDENT('abc')@6 OP('<')@9 NUMBER('10')@10
```

That example is the one that exposed the empty-set notation bug in
[regular-expressions](../regular-expressions/): with `0` reading as the empty
set, `(0|1)+` silently became `1+` and the lexer stopped on the `0` of `10`.
