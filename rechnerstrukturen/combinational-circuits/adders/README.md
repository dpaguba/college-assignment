# Adders

Each bit's sum is easy and its carry depends on every bit below, so the carry
chain is the whole problem.

    g_i = a_i and b_i          this position generates a carry
    p_i = a_i xor b_i          this position passes one through
    c_(i+1) = g_i or (p_i and c_i)

Unrolling that recurrence turns every carry into a two-level expression in the
generates and propagates, computable at once.

| adder | delay in gate delays at 32 bits |
|---|---|
| ripple carry | **64** |
| carry lookahead in groups of four | 14 |
| carry select | between the two |

The two adders are checked against each other on every 4-bit input pair: same
sums, same carries. An adder that is fast and occasionally wrong is worse than
a slow one, so the comparison is exhaustive rather than sampled.

## Subtraction reuses the same hardware

Invert the second operand and set the carry in. That is why an ALU has one
adder rather than two, and it is the practical argument for two's complement
that no amount of elegance would supply.
