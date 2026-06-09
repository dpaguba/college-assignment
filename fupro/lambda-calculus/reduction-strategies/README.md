# Reduction strategies

Contracting a redex is one rule. Which redex to contract first is the
strategy, and the strategies disagree about termination rather than about
results.

| Strategy | Contracts | Finds a normal form |
|---|---|---|
| normal order | leftmost outermost | whenever one exists |
| call by name | leftmost, not under a lambda | weak head normal form |
| call by value | argument first | not always |

```
(\x.\y.y) OMEGA
```

Call by name returns `\y.y`. Call by value evaluates the argument first and
never terminates, because `OMEGA` reduces to itself forever. Both are checked
here, and the discarded argument is the whole point: a strict language
computes something no one asked for.

## What the exam asks

The term `\x. (\y.y) (\z.z) (\a. x a)` reduces to `\x.\a.(x a)` in two steps,
and the module reports the intermediate terms rather than only the result.

## Confluence

Whatever order is used, the normal form is the same when there is one. That
is the Church-Rosser theorem, and the module checks it by reducing a term
under two strategies and comparing, which tests the implementation rather
than the theorem.
