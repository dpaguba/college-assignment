# Variance

A type constructor is covariant in a position when a function from a to b
gives a function from F a to F b, and contravariant when it gives one the
other way round.

The function type carries both. It is covariant in its result and
contravariant in its argument, because a function accepting more can be used
wherever one accepting less was expected. Nesting multiplies the signs, so a
position inside two arguments is covariant again:

| position | variance |
|---|---|
| result | covariant |
| argument | contravariant |
| argument of an argument | covariant |

Both cases are demonstrated rather than asserted. The reader functor, a
function from a fixed environment, maps by composing after, and a predicate
maps by composing before. The direction of the composition is the whole
difference, and it follows from which side of the arrow the parameter sits
on.
