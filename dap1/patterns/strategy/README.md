# Strategy

Chapter eleven and the tenth sheet, which asks for fourteen strategies against
one unchanged list.

The list gains four methods, one per kind of strategy, and never learns what
any of them compute:

| Method | Strategy | Sheet tasks |
|---|---|---|
| `traverse` | reads each value | 1 to 3 |
| `transformAll` | replaces each value | 4 to 6 |
| `removeAll` | decides what stays | 7 to 10 |
| `insertBehindSelected` | inserts behind selected values | 11 to 14 |

An object rather than a method, because a partial computation has state and it
has to live somewhere. The average of the positive values needs a sum and a
count between calls; the subtotal strategies need a running total; the
strategy that inserts from a second list holds an iterator over it. Putting
that state in the strategy is what keeps the list free of it.

## The wording decides the answer

`RemoveSmallerThanPredecessorStrategy` removes every value smaller than its
predecessor **in the original list**. Comparing against the last value kept
instead is the natural implementation and it is a different function:

```
5, 3, 4    original predecessor:  keeps 5 and 4
5, 3, 4    last value kept:       keeps 5 only
```

Both are reasonable readings of an English sentence and the sheet settles it
in a clause. The list makes the correct one possible by reading each
predecessor before anything is unlinked, so a removal never changes the
decision about the elements that follow.

## Insertion that terminates

The four insertion strategies insert behind the element they were shown, so a
strategy that selects everything would otherwise walk onto its own insertions
and never finish. The list steps past whatever it just inserted, which is the
one thing the traversal has to know that the strategy cannot.

`SubtotalOfThreeElementsStrategy` shows the state clearly: it inserts the
subtotal of three values behind every third element, and values left at the
end of the list enter no subtotal, which falls out of the counting rather than
needing a special case.
