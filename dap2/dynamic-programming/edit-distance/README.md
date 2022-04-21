# Edit distance

The fewest single-character edits turning one string into another.

| | |
|---|---|
| Time | O(n · m) |
| Space | O(n · m) |
| Table shape | two sequences |

## The idea

Three operations, each costing one: insert, delete, replace. The three neighbours of
a cell in the grid are exactly those three operations, which is the clearest
correspondence between a table and a decision anywhere in this folder.

## The recurrence

```
if left[i] == right[j]:  D(i-1, j-1)
otherwise:              1 + min(D(i-1, j),    delete
                                D(i, j-1),    insert
                                D(i-1, j-1))  replace
```

## What is worth noticing

It is a genuine metric: zero only for identical strings, symmetric, and it obeys the
triangle inequality. The tests check the last two on random input, because those
properties are what allow it to be used as a distance in clustering and nearest
neighbour search rather than merely as a score.

Recovering the operations is a backward walk. They come out in **descending
position order**, and applying them in that order is what keeps earlier edits from
shifting the indices of later ones. Applying them the other way round produces
plausible nonsense, which is how the test for this caught itself.
