# Fixed points

A recursive definition is an equation, and its solution is a fixed point of
the function describing one unfolding. The Y combinator produces that fixed
point, so anonymous functions alone are enough for recursion.

```
Y f  =  f (Y f)
```

That equation cannot be checked by reducing both sides to a normal form,
because neither side has one. The module checks it by reducing a few steps
and comparing, which is the most that can be said about a term that
deliberately never settles.

## Why there are two combinators

Under call by value, `Y f` diverges before it ever calls `f`, which the
module verifies. The Z combinator inserts an extra lambda so that the
recursive call is delayed until it is applied, and that delay is exactly what
a strict language needs. The same trick appears in Python, where `fix` has to
wrap the recursive call in a lambda for the same reason.
