# Control structures

A target machine has conditional and unconditional jumps and nothing else. Each
construct becomes a fixed pattern, and the patterns differ in cost.

| construct | conditional jumps | direct jumps |
|---|---|---|
| `while` | 1 | 1 |
| `do while` | **1** | **0** |
| `if then` | 1 | 0 |
| `if then else` | 1 | 1 |

## The published schemes

The lecture's `while`:

    lloop:
    code(cond)              // result in r0
    if r0 = 0 goto lexit
    code(body)
    goto lloop
    lexit:

and the `do while` the sheet asks for, with exactly one conditional jump
testing `r0 = 0` and no other jumps:

    lloop:
    code(body)
    code(!cond)             // result in r0
    if r0 = 0 goto lloop

Negating the condition is the whole trick. Testing `r0 = 0` on the negated
condition means "jump back while the condition holds", so the loop needs no
exit jump and simply falls through when it ends. The exit label disappears too,
because there is nothing to skip on the way in: the body runs before any test,
which is what the construct is for.

## The semantic difference, not just the shape

`run_while` with a condition that is false from the start executes the body
**0** times; `run_do_while` executes it **1** time. Whenever the condition holds
initially the two agree, checked for limits 1, 2, 5 and 10.

## `for` introduces nothing

A `for` loop is a `while` with the initialisation lifted out and the step
appended to the body. Writing the translation out makes that visible, and it is
the general pattern: most constructs that look new are one of these three in
disguise.
