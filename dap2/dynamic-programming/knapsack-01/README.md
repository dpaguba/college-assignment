# 0/1 knapsack

Pick items to maximise value without exceeding a weight limit.

| | |
|---|---|
| Time | O(n · capacity) |
| Space | O(n · capacity), or O(capacity) rolling |
| Table shape | capacity |

## The idea

0/1 means each item is taken whole or not at all, and that is what makes it hard: no
greedy rule is correct. Sorting by value per weight and taking greedily solves the
**fractional** version, where items can be split, and fails here. Weights 10, 20, 30
with values 60, 100, 120 and capacity 50: greedy takes the first two for 160, the
answer is the last two for 220.

## The recurrence

```
best(i, c) = max(best(i-1, c),  value[i] + best(i-1, c - weight[i]))
```

## What is worth noticing

**This is not polynomial time.** The input needs only log(capacity) bits to write
down, so a table of size capacity is exponential in the input length. Knapsack is
NP-complete, and this is a pseudo-polynomial algorithm: fast when the numbers are
small, useless when they are large. It is the distinction most people miss.

The rolling version uses one row and must walk capacities **downwards**. Upwards
would let an item be taken twice, because the cell it reads would already include
itself, and the answer silently becomes the unbounded knapsack. It also loses the
ability to say which items were chosen, because the rows that would be walked back
through were overwritten.
