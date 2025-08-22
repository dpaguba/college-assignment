# Instruction scheduling

Moving an unrelated instruction into a stall slot fills it. That is all static
scheduling is, and the limit is the dependence structure: a chain where each
instruction needs the previous one cannot be reordered at all, and the
scheduler correctly leaves it alone.

## Measured

A load, its use, and an independent subtraction cost one stall in that order
and none after scheduling, which moves the subtraction between them.

## Correctness is a separate check

`respects_dependences` verifies that every hazard kept its direction. Checking
it separately from the stall count matters, because a scheduler that reorders
freely removes every stall and computes the wrong answer. The scheduler here
refuses to cross WAR and WAW edges as well as RAW ones, since reordering across
them is unsafe without renaming.

## Unrolling makes the work that scheduling needs

Unrolling by itself only removes loop overhead. What makes it pay is that the
copies are independent **once renamed**, so the scheduler has something to fill
the stalls with. Renaming is not an optimisation of unrolling, it is the point
of it: two copies of a load-use pair still stall twice, and the unrolled and
scheduled version does not.
