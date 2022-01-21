# Dynamic array

Fixed storage that pretends to grow, by doubling when it fills.

| Operation | Cost |
|---|---|
| Index | O(1) |
| Append | O(1) amortised, O(n) worst |
| Insert or remove in the middle | O(n) |
| Search | O(n) |

| | |
|---|---|
| Memory | O(n), with up to half unused |
| Ordered | by position, not by key |

## The idea

Memory comes in fixed blocks, so an array cannot actually grow. What a dynamic
array does is allocate a larger block and copy across, and the only interesting
question is how much larger.

Growing by a constant, four slots at a time, makes n appends cost O(n²): each of
the n/4 reallocations copies everything so far, and 4 + 8 + 12 + ... is quadratic.
Doubling makes the same n appends cost O(n), because the copies are
1 + 2 + 4 + ... + n, a geometric series summing to less than 2n.

So an append is O(1) amortised while one append in every n is O(n). That is the
textbook case of amortised analysis, and the point it makes is that the worst case
per operation and the worst case per sequence are different questions.

## How it works

Keep a block, a capacity and a count. Append writes at the count and increments it;
when count reaches capacity, allocate double and copy.

Shrinking is deliberately lazy: at a quarter full, not a half. Halving at half
would make append, pop, append, pop at the boundary reallocate on every call.

## The trade

Indexing is arithmetic and the elements are contiguous, so it is as cache friendly as data gets. Inserting in the middle moves everything after it, which is what linked lists exist to avoid and rarely actually win.

## Where it is used

Python's `list`, Java's `ArrayList`, C++'s `std::vector`, Go's slices. It is the default sequence in every language that has one.
