# Merge sort

Merge sort against insertion sort on one harness. Practical sheet 2, tasks 2.2
and 2.3.

```
java Sortierung 6 merge ab
6 5 4 3 2 1
1 2 3 4 5 6
Feld ist sortiert!
Das Sortieren des Arrays hat 9 Vergleiche benoetigt.
```

Needs the previous task:

```
javac -sourcepath ../insertion-sort -d out Sortierung.java Laufzeitmessung.java
java -ea -cp out Sortierung 10000 merge rand
```

## The algorithm

Sort both halves, then merge them. T(n) = 2T(n/2) + Θ(n), the balanced case of
the master theorem, so Θ(n log n) on every input, unlike quicksort.

The scratch array is allocated once in the public method and handed down. An
allocation inside the recursion would be correct but would allocate Θ(n log n)
memory in total instead of Θ(n).

## The split is part of the specification

`mergeSort(l, r)` splits at `l + (r − l + 1)/2 − 1`, putting the smaller half on
the left. Splitting at the midpoint the other way is equally correct and
equally fast, and it gives 7 comparisons for six descending elements instead of
the 9 the sheet requires. Asymptotics do not pin down constants; the expected
output does.

## Counting comparisons in a merge

Only the head-to-head tests count. Once one side is exhausted the rest is
copied without comparing, which is why six descending elements cost 9 and not
15.

## Task 2.3: measurements

Five runs per size, median reported, milliseconds:

| n | insertion | merge | ratio |
|---|---|---|---|
| 1000 | 0.55 | 0.07 | 7.7 |
| 2000 | 0.33 | 0.08 | 4.2 |
| 4000 | 1.29 | 0.20 | 6.5 |
| 8000 | 5.12 | 0.44 | 11.7 |
| 16000 | 20.26 | 0.98 | 20.7 |
| 32000 | 81.21 | 1.94 | 42.0 |
| 64000 | 328.87 | 4.14 | 79.5 |

Doubling the input roughly quadruples insertion sort (20 → 81 → 329) and
roughly doubles merge sort. That is the two shapes, Θ(n²) against Θ(n log n),
visible without a chart.

The first two rows are noise: at that size the whole sort takes less than a
millisecond and the JIT is still warming up. That is why the sizes go up to
64000 and why the median of several runs is reported rather than one
measurement.
