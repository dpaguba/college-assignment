# Arrays

`Dim a(5)` creates **six** elements, indices zero to five: the number in the
brackets is the upper bound, not the length. With `Option Base 1` it is five,
indices one to five. This is the most common confusion with VBA arrays and
the reason to write `Dim a(1 To 5)` instead, which means the same thing
regardless of Option Base.

## ReDim Preserve

Changes the size and keeps the values. Growing adds empty elements; shrinking
drops the tail **without a warning**, which is the behaviour worth
remembering.

For a multi-dimensional array only the last dimension may be changed. The
reason is in the storage: values lie consecutively in memory, and changing an
earlier dimension would move every one of them.

## The starting value

Searching for the largest value in an array, the usual mistake is starting
from zero instead of from the first element. In an array of negative numbers
that finds zero, which is not in the array at all.
