# The simply typed lambda calculus

Three rules. A variable has the type the environment gives it, an abstraction
gets an arrow type, and an application requires the argument type to match
the domain.

The price is expressiveness. Self application cannot be typed, because the
same term would have to be both a function and its own argument, so `OMEGA`
has no type. That is not a defect: every typable term has a normal form, and
the terms that do not are exactly the ones the system rejects.

## The exam's inference

```
environment  x : (a -> b) -> a
term         \y. x (\z. y (x y))
type         (a -> b) -> a
```

Reproduced by the module. Getting it right needed one design decision: type
variables and type constants have to be different things. With both
represented as plain strings, the environment's base types `a` and `b` are
silently treated as unifiable variables, and the term comes back as an
infinite type rather than as its correct one.
