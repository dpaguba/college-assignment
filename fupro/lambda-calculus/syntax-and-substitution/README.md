# Syntax and substitution

Three forms: a variable, an abstraction, an application. Everything else in
the calculus is built from them, and all the difficulty is in substitution.

```
[y/x](\y.(x y))  must not give  \y.(y y)
```

Replacing `x` by `y` under a binder that happens to be called `y` would
capture the substituted variable and change its meaning. The fix is to rename
the binder first, which is why terms differing only in the names of bound
variables have to count as the same term.

The printer brackets an abstraction wherever it appears inside an
application. Without that, printing and reparsing changes the tree, because
the body of a lambda extends as far to the right as it can: `((\x.x) y)`
printed as `\x.x y` reparses as `\x.(x y)`.

All twenty-one terms of the lecture's `terms.txt` parse, which is the first
check the block performs.
