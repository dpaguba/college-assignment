# Doubly linked list

Chapter nine, with the course's own element class: a value, a predecessor and
a successor, and the list holding both ends and the size.

The second link is what the chapter is about. Removing an element needs the
one before it, and a singly linked list has to search for it, so removal is a
walk. Here the element already knows, so it is four assignments. Appending is
as cheap as prepending for the same reason on the other side.

Reversing shows it best. A singly linked list is reversed by a loop that
remembers three positions and rebuilds every link; here every element swaps
its two links and the head and tail are exchanged. No value moves, nothing is
allocated, and the loop body is symmetric.

The size is stored rather than counted, which is one field against a walk, and
the usual trade in this direction.

## Where the strategies attach

The tenth sheet adds four methods to this class, one per kind of strategy:
walk and report, replace each value, remove selected values, insert behind
selected values. The strategies themselves are in
[patterns/strategy](../../patterns/strategy/).

Two of them need care in the list rather than in the strategy. Removal passes
the predecessor **from the original list**, not the last value kept, because a
removal must not change the decision about the elements after it. Insertion
skips what it just inserted, so a strategy that selects everything terminates
instead of inserting behind its own insertions.

## Verification

400 random appends and removals against `java.util.ArrayList`, checking the
size after every step and the content at the end. The failures worth catching
here are the ones at the ends: removing the head, removing the tail, removing
the only element, and removing something that is not there.
