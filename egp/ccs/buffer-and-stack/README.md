# Buffer, stack and queue

Exercise sheet 5, and the block where the limits of the calculus show.

A buffer of capacity n has n+1 states, because all it needs to remember is
how many values it holds. An unordered buffer of capacity two needs four,
because it has to remember *which* values it holds. A stack of depth three
needs fifteen, because it has to remember the whole sequence.

| Process | What the state carries | States |
|---|---|---:|
| ordered buffer, capacity 3 | the count | 4 |
| unordered buffer, capacity 2 | the set | 4 |
| stack, depth 3 | the sequence | 15 |

## Stack against queue

The difference is one line. The stack pops the front of its content, the
queue the back. After `push0` then `push1` the stack offers `pop1` and the
queue offers `pop0`, and `what_comes_out_first` checks exactly that.

## Why the state grows

CCS has no data. A process remembers only which process it has become, so
everything it must remember has to be in the state name. That is why the
state count grows from n+1 to 2ⁿ to 2ⁿ⁺¹−1 as the requirement moves from
counting to sets to sequences, and it is the reason the π-calculus adds names
that can be passed.
