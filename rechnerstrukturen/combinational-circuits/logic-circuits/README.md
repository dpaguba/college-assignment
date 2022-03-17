# Gates and circuits

A circuit has a **size**, the gate count, and a **depth**, the longest path.
Size is area, depth is delay, and the same function usually admits a trade:
eight values combined in a chain and in a tree use the same seven gates and
have depths of **7** and **3**.

Rebalancing like that is licensed by associativity, which is why associativity
matters to a hardware designer rather than only to an algebraist.

## NAND is universal

Every function can be built from NAND alone, verified here for `not`, `and` and
`or` on every input combination. That is not a curiosity: it is why a
fabrication process is optimised for one gate.

## The building blocks

A **decoder** turns `k` bits into one of `2^k` lines. A **multiplexer** selects
one of `2^k` inputs, which is the hardware form of a conditional and the reason
a switch over a small range compiles to something without branches. An
**encoder** is the decoder's inverse and needs exactly one active input, which
is a real precondition rather than a formality.

## Fan-in is the constraint the maths ignores

Real gates take two to four inputs, so an eight-input AND is a tree with
logarithmic depth rather than a single gate with depth one. Ignoring that is
what makes a paper design look faster than the chip.
