# LOOP, WHILE and GOTO

Three tiny imperative languages over natural-number registers, in the course
because they make the Church-Turing thesis concrete: a model that looks nothing
like a tape computes exactly the same functions.

| Language | Adds | Halts always |
|---|---|---|
| LOOP | a loop with a count fixed when it starts | yes |
| WHILE | a loop on a register being non-zero | no |
| GOTO | labels and jumps | no |

## LOOP is strictly weaker, and that is a theorem

The count of a LOOP is read **once**. Changing the register inside the body
does not change how often it runs, and that single rule makes every LOOP
program terminate. The class it computes is exactly the primitive recursive
functions.

The Ackermann function is the witness that this is a real restriction, and it
is implemented here with an explicit stack in a WHILE loop, since the language
has no recursion:

```
A(0,2)=3   A(1,2)=4   A(2,2)=7   A(3,2)=29   A(3,3)=61
```

It grows faster than any primitive recursive function, so no LOOP program
computes it.

## The three conversions

- **LOOP to WHILE**: copy the count into a fresh register first, then count it
  down. Copying is the whole point, and skipping it changes the semantics.
- **WHILE to GOTO**: a test that jumps past the body, and a jump back at the
  end. That is what a compiler does with a loop, in ten lines.
- **GOTO to WHILE**: one loop over a program counter, with a chain of tests.
  The direction that looks harder is the one that shows the two are equally
  strong: a single unbounded loop can carry arbitrary control flow.
