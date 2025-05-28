# Shellsort

Insertion sort on elements a gap apart, with the gap shrinking to one.

| | |
|---|---|
| Best | O(n log n) |
| Average | depends on the gap sequence |
| Worst | O(n^(1+1/k)) for k gaps |
| Memory | O(1) |
| Stable | no |
| Family | insertion |

## The idea

Insertion sort moves an element one position per step, so an element far from home
is expensive. Shellsort first sorts the subsequences of elements that sit `gap`
apart, letting values cross most of the array in one move, then repeats with a
smaller gap. The final pass with gap 1 is plain insertion sort, by then on data
that is nearly ordered, which is exactly the case insertion sort is good at.

Nobody knows the optimal gap sequence. This is genuinely open: the best known
bounds come from experiment, not proof. This implementation uses Ciura's sequence,
1, 4, 10, 23, 57, 132, 301, 701, extended by a factor of 2.25.

## How it runs

1. For each gap in the sequence, largest first:
2. Run an insertion sort where "the previous element" means "the element `gap` back".
3. Finish with gap 1.

## When it is the right choice

Embedded code and anywhere the recursion of quicksort or the memory of merge sort is unwelcome. It is compact, in place, and fast enough up to tens of thousands of elements.
