# Searching

Linear and binary search, with the comparisons counted rather than argued.

| | 1024 sorted values |
|---|---:|
| linear search for the 500th | 500 comparisons |
| binary search for the same | 9 |
| binary search, worst case | 11 |

Eleven is the number of halvings of 1024, and no target exceeds it. That
number is the whole argument for keeping data sorted, and it is also the
argument for not doing so casually: the sort has to be paid for once, and it
only repays itself if enough searches follow.

The recursive and iterative versions are both here because the lecture gives
both, and they agree on 200 random targets including ones that are absent.
The recursion is the more readable of the two and the iteration avoids the
stack, which on this problem is a difference of style rather than of
capability.

Absence is the case worth writing a test for. A search that returns 0 for
"not found" is wrong for an array that holds the value at index 0, which is
why the convention is -1 and why the test asks for a value the array does not
contain.
