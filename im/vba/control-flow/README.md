# Control flow

## Exercise 11

Twenty places per tutorial. Under the old rule only fully occupied tutorials
ran; now half occupancy is enough.

With 95 students the old rule opens four tutorials and leaves fifteen
students without a place. The new rule opens five and leaves five seats
empty. With 85 students the new rule changes nothing, because five is below
half of twenty.

The function reports both the empty seats and the students without a place,
because under the old rule the second is the number that matters and the
first is zero.

## Offset

The exercise requires every cell to be addressed through B3. `Offset` counts
from the cell, and from zero: `Offset(0, 0)` is the cell itself. That is the
usual confusion, since rows and columns are counted from one everywhere else.
From B3, D7 is `Offset(4, 2)` and D10 is `Offset(7, 2)`.

## The one-line If

`If x > 0 Then y = 1` needs no `End If`, and that is a trap rather than a
convenience: adding a second statement later puts it outside the condition,
and the code still compiles.
