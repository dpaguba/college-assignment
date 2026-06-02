# Pattern matching

A pattern names a constructor and binds its arguments. Matching is therefore
a comparison and a binding, and the first equation that matches wins, which
is why a catch-all written first makes everything after it unreachable.

## Exhaustiveness

Because a type lists its constructors, whether a set of equations covers them
all is decidable. The module answers it, and reports which constructors are
missing rather than only that something is:

```
Maybe covered by [Just x]      ->  missing Nothing
Maybe covered by [_]           ->  exhaustive
```

A missing case is a run time error here, as it is in Haskell, and the point
of the check is that it can be made before running anything. That is a
property of algebraic data types rather than of pattern matching: an open
type would make the same question undecidable.
