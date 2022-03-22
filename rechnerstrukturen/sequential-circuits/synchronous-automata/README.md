# Moore and Mealy machines

A sequential circuit is a state register and two blocks of logic: next state,
and output. Where the output block gets its inputs is the whole difference.

| | output depends on | reacts | glitches |
|---|---|---|---|
| Moore | the state only | one cycle later | no |
| Mealy | the state and the input | immediately | inherits the input's |

Measured on the same input `1 0 0 0`: the Mealy machine outputs 1 in the first
step and the Moore machine outputs 0, catching up one step later.

## The conversion has a cost

Converting Mealy to Moore splits each state by the output that leads into it,
so the state count grows and the output sequence is delayed by one step. Both
are verified: the converted machine's output from step two onwards equals the
original's from step one.

That is the trade in one sentence: fewer flip-flops against a
worse-behaved output.

## From automaton to circuit

Encoding the states as bit vectors turns the transition table into one Boolean
function per flip-flop, to be minimised like any other. `ceil(log2 n)`
flip-flops suffice; a one-hot encoding uses `n` and makes the next-state logic
trivial, which is often the better trade in an FPGA and never in an ASIC.
