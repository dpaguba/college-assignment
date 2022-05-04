# Unbounded knapsack

The same problem, with an unlimited supply of each item.

| | |
|---|---|
| Time | O(n · capacity) |
| Space | O(capacity) |
| Table shape | capacity |

## The idea

Note what disappears from the state. In the 0/1 version the table has to record
which items are still available, so it is two-dimensional. Here every item stays
available for ever, so the amount alone is the state and the table is one row.

## The recurrence

```
best(c) = max over items i of (value[i] + best(c - weight[i]))
```

## What is worth noticing

In code the entire difference from the rolling 0/1 version is **the direction of the
inner loop**. Upwards lets a cell read a value that already includes the current
item, which is what taking it repeatedly means. Downwards forbids it.

One reversed loop separates two different problems, and writing it the wrong way
round is the most common way to solve the one you did not mean to.

Coin change is this problem with value equal to weight.
