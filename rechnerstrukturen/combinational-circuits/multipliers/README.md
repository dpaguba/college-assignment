# Multipliers

Multiplication is repeated addition of shifted copies, and the designs differ
in when the additions happen: one per cycle, all at once in a grid, or as few
as possible.

## Booth's recoding

A run of ones can be rewritten: `0111` is `1000 - 1`, so three additions become
one addition and one subtraction. Measured on `01111`, the sequential algorithm
performs 4 additions and Booth performs 2.

The recoding digit at position `i` is `y[i-1] - y[i]`, and summing
`digit * M * 2^i` gives the product with **no** correction term for a negative
multiplier: the telescoping sum works out to the two's complement value. That
is why Booth handles signed operands for free, verified over every pair in
`-8..7`.

## The trade between the two forms

| design | area | delay |
|---|---|---|
| shift and add | one adder | one cycle per bit |
| array | quadratic | linear |
| Wallace tree | quadratic | **logarithmic** |

A Wallace tree reduces three rows to two per level, so the depth is
logarithmic and the layout is irregular. That irregularity is the reason it is
used in a multiplier and nowhere else.
