# Tournament sort

A knockout bracket: the winner is the smallest, and replacing it replays only one path.

| | |
|---|---|
| Best | O(n log n) |
| Average | O(n log n) |
| Worst | O(n log n) |
| Memory | O(n) |
| Stable | yes |
| Family | selection |

## The idea

Play every element against a neighbour, winners advance, and after log n rounds one
element has beaten everybody. Take it out, and only the log n matches it played
need replaying: everything else in the bracket is unaffected.

This is a selection sort whose selection step costs log n, which makes it a sibling
of heapsort. The difference is that the whole bracket is retained, so the second
place is already known and the structure supports merging runs, which is why the
idea survives in external sorting under the name replacement selection.

## How it runs

1. Put the elements in the leaves of a complete binary tree, padding to a power of
   two.
2. Fill each internal node with the winner of its two children.
3. Output the root, empty its leaf, and replay the path from that leaf to the root.
4. Repeat n times.

## When it is the right choice

External sorting, where it generates runs twice as long as the available memory. Inside memory, heapsort does the same job without the extra array.
