# Random forests

Many trees, each on a sample drawn with replacement, each choosing among a
random subset of features at every node.

## What is left out

Drawing n points with replacement from n leaves each point out with
probability `(1 − 1/n)ⁿ`, which tends to `1/e ≈ 0.368`. Measured on 2 000
points: **0.372** left out against 0.3678 expected. Those points are unseen
data for that tree, so a forest can be measured without holding anything back.

## The forest against its own trees

| | error |
|---|---:|
| mean single tree | 0.242 |
| best single tree | 0.205 |
| **forest of 25** | **0.180** |

The forest beats even its best member. The mechanism is visible in the same
run: on 72.5 % of the test points the trees do not all agree, and it is exactly
that disagreement that averages out.

## Why both sources of randomness

Bagging alone is not enough. If one feature is much stronger than the rest,
nearly every tree puts it at the root and the trees end up similar; their
errors are then correlated and averaging buys little. Choosing among a subset
of features at each node forces some trees to work without the strong feature,
and only that makes them genuinely different.

The cost is that each individual tree gets worse. The ensemble is better anyway,
which is the part that is counter-intuitive until the numbers above are on the
table.
