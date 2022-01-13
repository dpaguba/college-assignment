# Elementary sorts

Five algorithms from chapter four and the fourth sheet, each with a counting
twin, because how much work they do depends on the input in ways worth
measuring.

Comparisons on 200 values:

| | ascending | descending | random |
|---|---:|---:|---:|
| selection | 19 900 | 19 900 | 19 900 |
| insertion | 199 | 19 900 | 9 727 |
| insertion with binary search | 1 345 | 1 153 | 1 266 |

Passes:

| | ascending | descending | random |
|---|---:|---:|---:|
| bubble | 199 | 199 | 199 |
| bubble, stopping early | 1 | 200 | 193 |

## The improvement that is not always one

The fourth sheet asks for insertion sort improved by finding the insertion
point with a binary search. On descending input it is seventeen times cheaper
in comparisons, and on already sorted input it is nearly seven times **more**
expensive: plain insertion stops after a single comparison per element, while
the binary search always performs its full seven or eight.

The improvement is real and it is not free. A binary search costs log n
comparisons whatever the data does, so it wins exactly where the linear scan
is long, and loses where the linear scan was going to stop immediately. Sorted
or nearly sorted input is common enough that this matters.

The moves tell the same story from the other side: the binary variant performs
the same number of array writes as the plain one, because knowing where a
value belongs does not help with shifting everything after it. Halving the
comparisons of an algorithm whose cost is dominated by moves buys less than
the comparison count suggests.

## Selection sort never notices anything

19 900 comparisons on every input of 200 values, which is 200 times 199 over
two. Sorted, reversed, random: the same. It always scans the entire remaining
range to find the smallest, so no arrangement of the data can make it faster
and none can make it slower. That predictability is its only advantage, along
with performing at most n exchanges, which matters when a move is expensive.

## Stopping early costs one pass

Bubble sort with the early exit finishes in one pass on sorted input and takes
200 on descending input, one more than the version without the check. The
extra pass is the one that establishes nothing changed. That is the shape of
most early exits: cheaper in the good case, marginally worse in the worst.

## Counting sort

Sorting by tallying performs no comparisons at all. It works because the
values are bounded, and the bound is the price: an array the size of the value
range. It is the first algorithm in the course that is faster than n log n,
and the reason it does not contradict the lower bound is that it never
compares two values.
