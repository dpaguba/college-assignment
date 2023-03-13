# Counting

Four ways to draw k things from n, and the formulas are easy to swap by
accident:

| | with replacement | without |
|---|---|---|
| ordered | n^k | n!/(n-k)! |
| unordered | (n+k-1 choose k) | (n choose k) |

For n = 5 and k = 3: 125, 60, 35 and 10. Each formula is checked against a
full enumeration of the draws for small cases, which is the point of having
both: the formula is fast and the enumeration is obviously right.

## The birthday problem

With 23 people the probability that two share a birthday is 0.5073, and with
22 it is below one half. The answer surprises because the question sounds
like it is about one person against the rest and is actually about all 253
pairs. Computing it directly as one minus the probability of all birthdays
being distinct makes that visible in the formula.
