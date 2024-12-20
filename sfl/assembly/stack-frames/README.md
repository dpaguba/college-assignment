# Stack frames

From the low address upwards: the local variables, the saved base pointer,
the return address. The stack grows downwards and a buffer is written
upwards, so an overflow runs straight into the saved data. The attacker does
not have to search for the return address; the direction of the write leads
there.

`build_frame` returns that layout with its offsets, and the `Stack` class
models push and pop with the pointer moving down and back up.

## The calling convention

System V on x86-64 passes the first six integer arguments in rdi, rsi, rdx,
rcx, r8 and r9, and the rest on the stack; the return value comes back in
rax. `place_arguments(8)` puts six in registers and two on the stack.

Callee-saved registers (rbx, rbp, r12 to r15) must come back unchanged;
caller-saved registers may not survive a call. Getting that wrong produces a
bug that appears only after some unrelated function is edited.

The prologue is `push rbp`, `mov rbp, rsp`, `sub rsp, n` and the epilogue
undoes it, with `leave` as the shorthand for the first two steps.
