# Dynamic branch predictors

A pipeline that resolves branches late must guess, and every wrong guess costs
the instructions fetched since. The predictors differ in how much history they
keep, and each extra bit buys one specific failure it stops making.

## The loop measurement

Four nested loops of "taken four times then not taken":

| predictor | mispredictions | accuracy |
|---|---|---|
| always taken | 4 | 0.800 |
| one bit | **7** | 0.650 |
| two bit | 4 | 0.800 |

The one-bit predictor is **worse than a fixed guess** here, and that is the
point of the example: after the loop exit it predicts not taken, so the first
branch of the next loop is wrong too. Two mispredictions per loop instead of
one.

The count is 7 rather than 8 because the initial state happens to match the
first branch, so the first loop pays only for its exit. A table quoting "two
per loop" is right about the steady state and wrong about the total.

## The second bit is hysteresis

The two-bit counter needs two consecutive disagreements to change its
prediction, which makes one exception noise rather than news. Verified
directly: after five taken branches, one not-taken leaves the prediction
unchanged and the second flips it.

## What neither can do

An alternating sequence defeats both: the one-bit predictor is right 2.5% of
the time, which is worse than chance because it is always exactly one step
behind, and the two-bit counter sits at 50%. Fixing that needs history, which
is [correlating-predictors](../correlating-predictors/).
