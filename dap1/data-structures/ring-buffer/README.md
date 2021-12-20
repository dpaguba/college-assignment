# Ring buffer

The seventh sheet. A fixed array with a read position and a write position
running around it, so a queue costs no allocation and no shifting.

The one ambiguity is that a read position equal to a write position means
either full or empty, and those are opposite. There are two ways out: store
the count, or leave one slot permanently unused so the two positions can never
coincide when full. The count is used here, since a field is cheaper than a
slot as soon as the values are larger than an int.

Verified against a reference list over 500 random operations, with the size
checked after each one. The interesting steps are the ones that wrap: writing
past the end of the array and reading past it afterwards, which is where an
off-by-one in the modulo shows up.
