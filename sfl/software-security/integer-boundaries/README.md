# Integer boundaries

A signed 32-bit value runs from −2147483648 to 2147483647. Adding two numbers
just above half of the maximum wraps into the negative: `exercise_inputs`
returns 1073742823 twice, whose mathematical sum is 2147485646 and whose
machine sum is **−2147481650**. That is exercise 3.1 solved, and the machine
arithmetic is modelled rather than the answer written down.

Unsigned subtraction wraps the other way: `0 - 1` in 32 bits is 4294967295.

## The length check that lets everything through

`length_check_bypass` shows the pattern that turns an arithmetic detail into a
memory corruption. The check compares a signed length against the buffer size,
so −1 passes it easily. The copy takes the length unsigned, where −1 is
4294967295, and copies that many bytes into a 64-byte buffer.

Two types, two readings of the same bit pattern, one check that guards
nothing. The module reports the check passing and the byte count together.

Widening keeps the sign, so −1 stays −1; narrowing does not, so 256 in eight
bits is 0. Where those conversions happen implicitly is where the surprises
are: a size computed by multiplication, a difference that can go below zero,
an index derived from input.
