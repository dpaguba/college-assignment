# Strand sort

Pull out the runs that are already sorted, merge them one by one.

| | |
|---|---|
| Best | O(n) |
| Average | O(n²) |
| Worst | O(n²) |
| Memory | O(n) |
| Stable | yes |
| Family | merge |

## The idea

Walk the remaining input and take every element that is not smaller than the last one
taken. That subsequence, the strand, was already in order. Merge it into the output
and repeat with what is left.

The running time is a direct measure of how ordered the input already was. Sorted
input yields one strand and costs linear time. Reversed input yields n strands of
one element each and costs n².

## How it runs

1. Take the first remaining element, then sweep the rest collecting everything not
   smaller than the last one taken.
2. Merge that strand into the output.
3. Repeat until nothing is left.

## When it is the right choice

Linked lists, where the repeated extraction costs nothing, and data known to arrive in long ordered stretches.
