# Flip-flops

Two cross-coupled NOR gates hold one bit, because each gate's output is the
other's input. Setting `S` drives the output to one, setting `R` drives it to
zero, setting neither holds.

## Why R = S = 1 is forbidden

The exercise asks, and the answer has two halves.

**Statically**, both outputs are forced to zero, so the invariant that the
second output is the complement of the first is violated. The flip-flop is in a
state its own definition does not have, which is what `rs_raw` reports:
`q == not_q`.

**Dynamically**, releasing both inputs at once leaves both gates seeing zeros,
both switching to one, then both seeing ones and switching back. The trace
oscillates, and which state it eventually settles in depends on which gate is
faster. A circuit whose state depends on manufacturing tolerances is unusable,
which is the real objection: not that the standard forbids it, but that the
physics does not decide it.

## The three answers to that problem

| flip-flop | what it does with the case |
|---|---|
| D | makes it unreachable, by driving `R` with the complement of `S` |
| JK | gives it a meaning, namely toggle |
| T | JK with the inputs tied together, so it always toggles |

A chain of T flip-flops divides a clock by two per stage, verified as the
alternating output sequence, which is what a ripple counter is.

## Setup and hold

A flip-flop samples at the clock edge and needs its input stable from `setup`
before until `hold` after. Violating the window leaves it **metastable**,
sitting between the two logic levels for an unbounded time. Metastability
cannot be designed away, only made improbable, which is why crossing a clock
domain costs two flip-flops and an argument.
