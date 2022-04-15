# Fibonacci

Assignment 0, the C warm-up. Two implementations of the same function, and the
gap between them is the point.

The recursive version reads like the definition and spawns two calls per call,
so the number of calls is itself a Fibonacci number and the time is
exponential. The iterative version carries two values forward and is linear,
because the recursion recomputed the same subproblems and the loop does not.

The program refuses `n > 90`, where the result overflows an unsigned 64-bit
integer, and skips the recursive computation above `n = 30`, where it stops
being instant.

```
gcc -std=c11 -Wall -Wpedantic -Werror -o fibonacci fibonacci.c
./fibonacci
```

## Input validation is the actual exercise

`scanf` returns how many items it converted, so a non-numeric input returns
zero rather than failing loudly, and the variable keeps whatever it held.
Checking that return value is the whole of the validation the assignment asks
for, and it is the part most submissions leave out.
