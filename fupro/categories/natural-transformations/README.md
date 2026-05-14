# Natural transformations

A map between functors is natural when it commutes with mapping:

```
fmap f . transform  =  transform . fmap f
```

The square says the transformation may rearrange the structure and may not
look at what is inside it. Taking the head of a list, reversing a list and
taking the length are all natural; a transformation that filters on the
values is not, and the module finds the failure by mapping a function that
changes them.

That is the formal content of the slogan that a polymorphic function cannot
inspect its arguments. A function of type `[a] -> Maybe a` knows nothing
about `a`, so whatever it does has to be the same before and after the
values are replaced, and being natural is exactly that.

The length is the case that looks odd and is not: its target is the constant
functor, whose map does nothing, so the square says the length is unchanged
by mapping.
