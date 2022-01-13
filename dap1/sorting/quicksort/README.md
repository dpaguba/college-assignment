# Quicksort

Comparisons on 200 values:

| Pivot | ascending | descending | random |
|---|---:|---:|---:|
| last element | 19 900 | 19 900 | 1 570 |
| middle element | 1 153 | 1 225 | 1 652 |

The lecture's version takes the last element of the range. On sorted input
every partition splits off one element and the rest, so the recursion is 200
levels deep and the comparison count is the same 19 900 that selection sort
needs. The algorithm whose reputation is speed is at its worst on the input
that most needs no work at all.

Taking the middle element instead costs 1 153 on the same input. It is not a
cure: for any fixed rule there is an input that defeats it, and the fix in
practice is a random or median-of-three pivot, which makes the bad case
unlikely rather than impossible.

## The pivot rule that is better is also worse

On random input the last-element pivot needs 1 570 comparisons and the middle
pivot needs 1 652. The rule that avoids the disaster is slightly slower when
there is no disaster to avoid, because moving the middle element to the end
before partitioning costs an exchange per call.

That is the trade in one table: a worst case seventeen times better, an
average case five percent worse.

## Partitioning is the whole algorithm

Everything quicksort does happens in the partition step, and the invariant it
establishes is what the recursion needs: the pivot is at its final position,
everything before it is at most the pivot, everything after is at least. The
recursion then never touches the pivot again, which is why quicksort needs no
merge step and sorts in place.
