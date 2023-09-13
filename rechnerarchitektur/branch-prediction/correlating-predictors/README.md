# Correlating and tournament predictors

A saturating counter learns the bias of one branch and cannot learn a pattern.
A correlating predictor keeps the last `k` outcomes and uses them to select
among `2^k` counters, which turns a pattern into several constant sub-patterns.

## On the alternating sequence

| predictor | accuracy |
|---|---|
| always taken | 0.500 |
| one bit | **0.025** |
| two bit | 0.500 |
| correlating, 1 history bit | **0.950** |
| tournament | 0.950 |

One bit of history is enough, because after a taken branch the next is always
not taken and vice versa. The one-bit predictor's 2.5% is the worst possible
result and is not bad luck: it is always exactly one step behind.

## The table doubles per history bit

Two history bits need four counters, four bits need sixteen. That exponential
is why real designs share counters between branches and accept the aliasing
rather than paying for a private table.

## Tournament predictors

Two predictors and a chooser that learns which to trust, per branch. The
chooser updates **only when the two disagree**, since agreement says nothing
about which is better, and that detail is what keeps it from drifting.

The point is not that it wins everywhere but that it never loses badly: it
tracks the better of its two components on every pattern tried, which is what a
real workload with a mix of branch kinds needs.
