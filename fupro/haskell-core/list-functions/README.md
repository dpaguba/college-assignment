# List functions

The functions the lecture builds by hand before using them: map, filter, zip,
takeWhile, append, reverse, and quicksort written with two comprehensions.

```haskell
quicksort (p:xs) = quicksort [x | x <- xs, x < p] ++ [p] ++ quicksort [x | x <- xs, x >= p]
```

No indices, no swaps, no loop. What the definition leaves out is what the
imperative version spends most of its lines on, and what it gives up is doing
the work in place.

## The transitive closure

The example of the fourth lecture, computed as a least fixed point: add the
pairs that a two-step path allows until nothing new appears. The relation
`1<2, 2<3, 3<4` closes to six pairs, and closing an already closed relation
changes nothing, which is what "fixed point" means and what the module
checks.
