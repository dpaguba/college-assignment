# The monad laws

```
return a >>= f   =  f a
m >>= return     =  m
(m >>= f) >>= g  =  m >>= (\x -> f x >>= g)
```

Nothing in the type system enforces them, so an instance can typecheck and be
wrong. The module includes such an instance and the first law catches it.

The third law is what makes do-notation a notation: it expands to a chain of
binds, and associativity is what allows the lines to be regrouped without
changing the meaning. The module checks that a do-block and the corresponding
bind chain compute the same value, which is the claim the translation in the
exam rests on.

Laws that a compiler cannot check are the recurring theme of this whole
block. They are checked here the only way available: by running both sides on
samples and comparing.
