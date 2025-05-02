# Flashsort

Predict where each element belongs, permute it there in one pass, finish with insertion sort.

| | |
|---|---|
| Best | O(n) |
| Average | O(n + r) |
| Worst | O(n²) |
| Memory | O(m) |
| Stable | no |
| Family | non-comparison |

## The idea

The n log n lower bound is a statement about comparison sorts: any algorithm that
learns about the data only by asking "is a < b" needs at least log₂(n!) questions.
Every sort in this family sidesteps the bound by looking at the key itself instead
of comparing keys, so the proof simply does not apply to them.

Neubert's algorithm. A linear map from the key range onto about 0.42·n classes
predicts each element's class. Counting the classes gives their boundaries, and the
elements are then permuted into place by following cycles, so no second array is
needed. What remains is nearly sorted, and one insertion sort pass finishes it.

It is bucket sort that refuses to allocate the buckets. The speed comes from that,
and so does the fragility: keys far from uniform pile into one class and the final
insertion sort turns quadratic.

## How it runs

1. Find the minimum and maximum, and classify every key linearly between them.
2. Count the classes and turn the counts into boundaries.
3. Permute in place: carry each displaced element to its class and pick up whatever
   was there.
4. Insertion sort the result, which is almost ordered already.

## When it is the right choice

Large numeric arrays with a known, roughly uniform distribution, where the O(1) extra memory matters.
