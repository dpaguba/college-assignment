# Sorting

| Topic | |
|---|---|
| [elementary-sorts](elementary-sorts/) | selection, insertion, bubble, counting |
| [quicksort](quicksort/) | partitioning, and what the pivot decides |

Every algorithm here has a counting twin, because the interesting property of
a sorting algorithm is how its work responds to the input. Selection sort
performs 19 900 comparisons on 200 values whatever they are. Insertion sort
performs 199 on sorted input and 19 900 on reversed input. Quicksort with the
lecture's pivot performs 1 570 on random input and 19 900 on sorted input,
which is the same number, reached from the opposite direction.

Two results here contradict the way the improvements are usually presented.
Insertion sort with a binary search is nearly seven times more expensive than
the plain version on sorted input. Quicksort with a middle pivot is five
percent slower than the last-element pivot on random input. Both improvements
are worth making, and both are worth measuring before being believed.
