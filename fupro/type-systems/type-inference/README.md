# Type inference

The algorithm invents a fresh variable wherever the term does not say what
the type is and calls unification wherever the rules force an agreement. What
comes back is the principal type: every type the term has is an instance of
it.

| term | principal type |
|---|---|
| `\x.x` | `t0 -> t0` |
| `\x.\y.x` | `t0 -> t1 -> t0` |
| `\f.\x.(f x)` | `(t1 -> t2) -> t1 -> t2` |
| `\f.\g.\x.(f (g x))` | `(t3 -> t4) -> (t2 -> t3) -> t2 -> t4` |
| `\x.(x x)` | none |

The last line is the point of the whole system, and the last but one is the
point of inference: composition gets its type without anyone writing a
signature, and the type is the most general one, so the same definition
serves every use.

The module also checks that a specific type such as `int -> int` is **not**
the principal type of the identity. An inference that quietly commits to a
concrete type still typechecks the program that produced it and rejects the
next one.
