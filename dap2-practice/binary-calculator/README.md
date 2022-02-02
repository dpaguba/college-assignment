# Binary calculator

Not from the practical sheets: this one was written outside the course
exercises and is kept here because it was worth finishing.

Addition, subtraction and multiplication of binary numbers, digit by digit.

```
java BinaryCalculator 1011 '*' 110
1011 * 110 = 1000010
```

Run it without arguments for the interactive prompt.

## What the exercise is about

The operands stay as strings of `0` and `1` from start to finish. Parsing them
into `int`, using `+`, and printing the result with `Integer.toBinaryString`
produces the right answer while skipping the entire exercise, and it also caps
the operands at 32 bits. Here the only limit is memory.

## The three operations

**Addition** is ripple carry: walk from the least significant digit, add the
two digits and the incoming carry, keep the low bit and pass the high one on.
Θ(n), and optimal, because flipping any input digit changes the answer so every
digit has to be read.

**Subtraction** borrows instead of carrying. The sign is handled by comparing
the magnitudes first and always subtracting the smaller from the larger.
Two's complement would be the alternative and it needs a fixed width agreed in
advance; comparing costs one extra pass and keeps the operands unbounded.

**Multiplication** is shift and add: for every `1` in the right operand, add the
left operand shifted by that position. Θ(n·m), the schoolbook method, and the
one [Karatsuba](../../dap2/divide-and-conquer/karatsuba/) improves on by
replacing four half-sized products with three.

## Verification

Twenty thousand random operand pairs of up to 40 bits, all three operations
checked against `BigInteger`. Subtraction was checked in both orders so the
negative branch is exercised.

## What was wrong with the original

It parsed both operands with `Integer.parseInt(s, 2)` and did the arithmetic in
`int`, so it demonstrated nothing about binary arithmetic. It also required
both operands to have the same number of digits, which is a restriction the
algorithms do not need: the loops simply treat a missing digit as zero.
