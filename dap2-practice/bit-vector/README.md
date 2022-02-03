# Bit vector with rank and select

Three succinct data structures. Practical sheet 9.

```
java Example
Bitvektor: 0100110111100010101011
rank(10) = 6
count(2, 9) = 4
select(8) = 14
select(3, 5, 12) = 8
```

## BitVector

n bits packed into ⌈n/32⌉ integers. Position j is bit j mod 32 of word j/32,
and both are a shift and a mask because 32 is a power of two.

A `boolean[]` would take a whole byte per entry, eight times more, because the
JVM has no addressable unit smaller than a byte. That factor of eight is the
exercise.

## BitVectorRank

`rank(i)` counts the 1-bits before position i. The bit at the query position is
not counted, which makes rank(0) = 0, rank(n) the total, and `count` a plain
subtraction.

One prefix sum is stored per block of 1024 bits, so the structure costs
32·n/1024 = n/32 bits, inside the ⌈n/25⌉ + 3200 the sheet allows. A query starts
from the nearest sample, adds whole words with `Integer.bitCount`, and masks off
the tail of the last word: at most 32 popcounts, a constant, and popcount is a
single instruction on any processor of the last fifteen years.

Precomputing the answer for every position would also be O(1), and would cost
32n bits: thirty-two times the vector it is meant to help. The whole subject of
succinct data structures is that gap.

## BitVectorSelect

`select(k)` is the inverse of rank, found by binary searching over it in
O(log n) with no extra memory at all. That is the cheap way to invert any
monotone query. Real succinct structures answer select in constant time too,
with a second sampled index, which costs space this task forbids.

The windowed `select(k, start, end)` reduces to the global one: the k-th one in
the window is the (rank(start) + k)-th overall, and it only counts if it lands
before the end.

## Static by design

The sheet allows it, and the samples would all be stale after a single `set` on
the underlying vector.

## Verification

The sheet prints the expected output of its own example program in full, and
every one of those 45 lines matches. Beyond that, 40 random vectors of up to
5000 bits were checked position by position against a plain `boolean[]`, for
rank, count, both forms of select, and the out-of-range cases.
