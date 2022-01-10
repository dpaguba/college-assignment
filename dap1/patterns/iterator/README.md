# Iterator

Chapter ten. Two methods, `hasNext` and `next`, and the code that walks a
structure stops knowing how the structure stores anything.

The gain is measured in classes that do not have to exist. Comparing two lists
element by element is one method here, and because it takes iterators rather
than lists it also compares a list with a tree walk, or either with the
multi-list iterator, without a line of new code. Without the interface, every
pair of structures needs its own comparison.

## Different walks, same structure

The reverse iterator adds no method to the list. It is a class that walks the
existing links from the other end, which is why a structure can be traversed
in ways it was never written for. That is the part of the pattern that is easy
to miss: the iterator is not only a way to hide the structure from the
algorithm, it is a way to add traversals without touching the structure.

## Where the empty case bites

The multi-list iterator from the ninth sheet runs over several lists in
sequence, and the awkward case is an empty list in the middle. After
finishing one list, the iterator has to skip every empty list that follows
before it can answer whether a further value exists.

Doing that in `hasNext` rather than in `next` is what keeps the answer
correct, and it is why `hasNext` here is not a pure query. An implementation
that advances only in `next` reports that a value exists and then fails to
produce one.
