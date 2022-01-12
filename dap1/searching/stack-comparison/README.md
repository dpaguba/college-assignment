# Two stacks of exam papers

The first sheet asks five questions about two piles of about 500 papers, and
then asks what changes when the piles are sorted. The published solution gives
the answer as a count.

| Two arrays of 500 | Comparisons |
|---|---:|
| counting the common numbers, unsorted | 194 389 |
| the same, sorted | 666 |

Two hundred and ninety times fewer, from one property of the data. The
unsorted version has to look at the whole second pile for every paper in the
first; the sorted version walks both at once and never goes back, because a
number already passed can never appear again.

## The question that cannot stop early

The five questions are not equally expensive, and the reason is where they may
stop. "Is there at least one student in both?" ends at the first match. "Is
there none?" is its negation and ends at the same place. "How many?" cannot
stop at all, because the count is only complete when everything has been seen.

The last two questions turn on a different observation: whether every number
in the first pile exceeds every number in the second is a question about two
numbers only, the smallest of the first and the largest of the second. Asking
it as a nested loop over both piles is 250 000 comparisons for an answer that
needs 1000.
