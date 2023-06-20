# CYK

The word problem for context-free grammars, in cubic time.

The grammar must be in [Chomsky normal form](../chomsky-normal-form/), and that
requirement is what makes the algorithm work: a substring of length one is
covered by a single rule, and a longer one splits into exactly two parts whose
covering variables are already known.

```
  len 5:      S
  len 4:      -            X1
  len 3:      S            -            S
  len 2:      -            X1           -            X2
  len 1:      S            W+           S            W*           S
              a            +            a            *            a
```

O(n³·|G|) time, O(n²) space. A regular language is decided in linear time; this
is the general bound one level up, and the gap is the price of the stack.

## Counting instead of enumerating

`count_parses` fills the same table with numbers rather than sets. The number
of parse trees can grow exponentially while the table stays cubic, which is
what makes the ambiguity check in
[context-free-grammars](../context-free-grammars/) affordable.

On the classic expression grammar, `a+a*a` comes out with **2** trees, which is
exactly the ambiguity that forces precedence rules into every real grammar for
arithmetic.

## Reading the tree back

`parse_tree` walks the filled table downwards, choosing any rule and split
whose halves are covered. Which tree comes out depends on the order the rules
are tried, and that freedom is precisely what an ambiguous grammar leaves open.
