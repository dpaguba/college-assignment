# Binary addition

Add two numbers held as bit arrays, without converting them to integers.

| | |
|---|---|
| Time | Θ(n) bit operations |
| Space | Θ(n) for the result |
| Optimal | yes, every input bit must be read |

## The idea

Schoolbook ripple-carry addition. Walk both operands from the least
significant end, add the two bits and the incoming carry, keep the low bit of
the sum and pass the high one to the next position. The result is at most one
bit longer than the longer operand.

## Why not just use `+`

Because the cost is the entire point. `int(''.join(...), 2) + int(...)` gives
the right answer and hides the only thing being studied: that adding two n-bit
numbers costs Θ(n) bit operations, and that this is the unit in which every
other arithmetic algorithm is priced.

Θ(n) is also a lower bound. Flipping any single input bit changes the answer,
so no algorithm can skip reading one.

## Why it sits in this folder

Addition is not divide and conquer. It is here because it is the linear-time
primitive that [karatsuba](../karatsuba/) is measured against: the recurrence

```
T(n) = 3T(n/2) + O(n)
```

has additions in its combine step, and the whole argument that three
multiplications beat four depends on additions being cheap enough to ignore.
Reading the O(n) term as a real piece of code makes the recurrence concrete
rather than symbolic.

## What is worth noticing

The same routine is what a hardware adder does, one full adder per bit, with
the carry rippling along the chain. That ripple is the latency, which is why
real processors use carry-lookahead adders instead: they compute in O(log n)
depth what this loop does in n steps, at the cost of far more gates. Sequential
Θ(n) and parallel Θ(log n) are the same algorithm under two different cost
models.
