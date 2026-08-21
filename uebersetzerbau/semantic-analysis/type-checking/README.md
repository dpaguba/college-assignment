# Type checking

A typing judgement is written `L, C, M, V |- e : t`: under a class table `L`,
inside class `C`, in method `M`, with variables `V`, the expression `e` has
type `t`. A program is type-correct exactly when a derivation exists.

Implementing it as a derivation rather than as a boolean pays off when a
program fails to check: the partial derivation says which premise could not be
established, which is the difference between a usable error message and "type
error".

## The published fragment

    B x; if (x == null) x = (B)this;

checked inside class `C`, where `B` is a subclass of `C`, derives as

```
      declare : void
          var : B
          null : null
        eq : boolean
            this : C
          cast : B
        assign : void
      if : void
    seq : void
```

It is **statically type-correct**, and it throws **ClassCastException** when it
runs. Both halves are reproduced: the checker accepts it, and the small
interpreter reports the exception when `this` really is a `C` and reports `ok`
when the object happens to be a `B`.

The gap is the point of the exercise. The checker reasons about the *declared*
type of `this`, which is the class the code sits in. `this` is not assignable,
so it is definitely a `C`, and a downcast to `B` cannot succeed. A type system
that rejected this would also reject every downcast that does succeed, which is
why the check is deferred to run time instead.

## The rules that make it work

| expression | rule |
|---|---|
| `null` | has the artificial null type, assignable to every class type |
| `this` | has the type of the enclosing class |
| `(B) e` | allowed when `B` and the type of `e` are on one chain, in either direction |
| `x = e` | allowed when the type of `e` is a subtype of the type of `x` |
| `e1 == e2` | boolean, when one side is assignable to the other |

A cast between unrelated classes is rejected statically, because no object can
ever have both types. Comparing unrelated classes is rejected for the same
reason.

## One defect the tests did not catch

Checking a fragment declared its variables in the checker's own scope, so
checking the same fragment twice raised a redeclaration error. Every test used
a fresh checker, so all sixteen passed. Statements are now checked inside a
fresh scope, which is both correct as Java semantics, a block is a scope, and
what any tool inspecting a program more than once needs.
