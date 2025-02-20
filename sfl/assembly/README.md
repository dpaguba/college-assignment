# Assembly

Three modules covering what the software security block needs: the flags a
comparison leaves behind, the instruction pointer under call and return, and
the layout of a stack frame.

Both exercise sheets' published answers are reproduced: the flag values after
`cmp eax, ebx` and after the mask sequence, and the instruction pointer at 2,
7, 3 and 1234.

The frame layout is the bridge to the next block. Locals below, saved base
pointer and return address above, a buffer written upwards: that geometry is
the whole reason a stack overflow takes control rather than merely corrupting
data.
