# The board

The board is not looked up, it is constructed. Nineteen hexes in rows of
3-4-5-4-3, in integer coordinates: two units along a row, three units between
rows. Every corner of every hex then lands on an exact integer pair, so shared
corners coincide without rounding.

| | |
|---|---:|
| hexes | 19 |
| intersections | 54 |
| roads | 72 |
| adjacent hex pairs | 42 |

## Euler checks the construction

For a connected planar graph, `V − E + F = 2`, where the faces are the
nineteen hexes and the outside. Here: `54 − 72 + 20 = 2`. The formula knows
nothing about Catan, so if a corner were counted twice or an edge missed, it
would not come out at two. That is the whole point of using it.

The same construction, redone in floating-point hex geometry with a
circumradius of one, gives the same 54 and 72.

## Where the intersections sit

36 have three roads and 18 have two. The second group is the border, and it is
a third of the board: a settlement there touches at most two hexes instead of
three, which is the geometric reason the edge of the board is weak.

## What the counting settles

Four players hold twenty settlements between them. With the distance rule
blocking every neighbour of an occupied corner, the board is tight long before
the pieces run out, and that is why the two opening placements decide so much.
