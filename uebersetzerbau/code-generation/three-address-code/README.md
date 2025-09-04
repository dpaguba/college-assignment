# Three-address code

Each instruction has an operator and at most three addresses. A tree of
arbitrary depth becomes a flat list, with temporaries holding what used to be
subtrees:

    2 + 3 * 4     becomes     t0 := 3 * 4
                              t1 := 2 + t0

Flattening is what makes the later phases possible. A register allocator needs
to know when a value is live, an optimiser needs to compare expressions, and
neither can do that on a tree where a value has no name.

Temporaries are numbered in evaluation order, because the generator is
post-order: an operator needs its operands' names before it can be emitted.
That is also the order a stack machine would push them in, which is why the two
representations convert into each other so easily.

## Checked by running it

The generated code and the original tree must produce the same number. That is
a much stronger check than inspecting the instruction list: `2+3*4` gives 14,
`(2+3)*4` gives 20, and `10-3-2` gives 5 rather than 9.

## What it does not do

`a*b + a*b` generates three instructions, not two. Recognising that the two
multiplications are the same computation is
[available-expressions](../../optimisation/available-expressions/), a separate
analysis on a separate pass. Generating naive code and then improving it is not
laziness, it is what keeps the generator simple enough to be correct.
