# Clipping and rasterisation

Cohen-Sutherland gives each endpoint a four-bit code for the regions it is
outside of. Both codes zero means the segment is inside and is kept whole; a
non-empty bitwise and means both ends are beyond the same edge and the
segment is dropped without any arithmetic. Only the remaining cases cost a
division.

The implementation is checked against a sampling of the segment: 300 random
segments are walked in 500 steps each, and the part inside the window is
compared with what the algorithm returns.

## Bresenham

The line is rasterised with an error term and integer additions only, no
multiplication and no division. Over 200 random lines the largest distance
from a chosen pixel to the ideal line was 0.4996, which is the bound the
algorithm promises: never more than half a pixel.

Reversing the endpoints produces the reversed pixel list, so the line does
not depend on which end it is drawn from.
