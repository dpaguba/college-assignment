# Folds and unfolds

A fold replaces every constructor by a function, so it is determined by one
function per constructor and nothing else. Every recursive function over a
list can be written as one, which is why the exam asks for the fold of the
binary numbers before asking for anything that uses it.

The two directions are not interchangeable:

```
foldr (-) 0 [1,2,3]  =  2
foldl (-) 0 [1,2,3]  = -6
```

They agree exactly when the operation is associative with the starting value
as its unit, which is the same condition as being a monoid, and that is the
connection this block shares with the homomorphism module.

An unfold is the dual: it produces a structure from a seed until the step
says to stop. A fold after an unfold is a loop, and writing it that way
separates what is produced from what is consumed.
