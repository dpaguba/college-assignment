# Higher-order functions

In a curried language every function takes one argument and returns a
function, so applying it to fewer arguments than it appears to need is
ordinary rather than special.

```
curry   :: ((a, b) -> c) -> a -> b -> c
uncurry :: (a -> b -> c) -> (a, b) -> c
```

The two are inverse, which the module checks by composing them. That
isomorphism is why a two-argument function has a type with two arrows and why
partial application needs no special support: `add 5` is a value like any
other.

Composition, flip and the constant function complete the set. They are the
functions with no content at all, which is exactly why they can be given a
type that says everything about them: the identity has type `a -> a` and
there is only one function with that type.
