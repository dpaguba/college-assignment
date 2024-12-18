# Control flow

`call` pushes the address of the following instruction and jumps; `ret` pops
it back into the instruction pointer; `jmp` goes where it says and leaves the
stack alone.

## Exercise 2.2

With the line numbers used as addresses:

| after | rip |
|---|---|
| `mov rbx, 5` | 2 |
| `call double` | 7 |
| `ret` | 3 |
| `jmp 1234` | 1234 |

The call goes to 7, the first instruction inside `double`, and leaves 3 on
the stack; the return takes it back. These are the published values.

A return without a preceding call has nothing to pop, and the module raises
rather than inventing an address. That empty stack is exactly what a buffer
overflow fills.

## The conditional jumps

`equivalent` compares two jump names over all sixteen flag combinations, so
`je` and `jz` come out identical and `jb` and `jl` do not. The unsigned family
reads the carry flag, the signed family compares sign against overflow. Both
answer "less than" and they answer it about different arithmetic.
