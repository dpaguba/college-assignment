# Exponential smoothing

s(t) = α x(t) + (1 − α) s(t − 1), starting from the first observation. The
exercise asks for α of 0.1, 0.2 and 0.3.

## The recursion is the weighted sum

Written out, the smoothed value is a weighted sum of all past observations
with weights α, α(1 − α), α(1 − α)², and the remainder (1 − α)ⁿ still sitting
on the starting value. The module computes both and they agree to 1e-9 for
all three α, and the weights plus the remainder sum to exactly one at every
truncation.

That remainder is the reason the sum of the first forty weights at α = 0.3 is
0.9999994 and not 1: (1 − 0.3)⁴⁰ = 6.4e-7 is still on the start.

## What it cannot do

On a straight line rising by 1 per step, the smoothed series settles a fixed
distance behind, and that distance is (1 − α)/α: measured 2.3333 at α = 0.3
against a predicted 2.3333. Simple exponential smoothing has no trend term,
so its forecast for every horizon is the same last smoothed value. A series
with a trend needs a second equation for it.

A smaller α smooths more and lags more. α = 1 reproduces the series exactly
and smooths nothing.
