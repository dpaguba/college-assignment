# Evaluating a policy without playing it

Weight each logged action by the ratio of the two probabilities: how often the
policy under study would have chosen it, over how often the logging policy
did. The estimator is unbiased as long as the logging policy plays every
action the studied one plays.

Measured over 600 logs: **0.7999** against a true value of 0.8.

## Unbiased and unusable

As the two policies move apart, the estimate stays right on average and its
spread grows without bound:

| how far apart | mean estimate | spread |
|---:|---:|---:|
| identical | 0.800 | **0.055** |
| far | 0.764 | **0.725** |

A single estimate is then worthless while the method is still correct. That
confusion between being unbiased and being reliable sits behind a good number
of results that look too good.

## The winner's curse, again

Forty policies, all in truth equally good, all scored on the same log; the
best-scoring one is taken:

| candidates | reported value | true value | on a fresh log |
|---:|---:|---:|---:|
| 1 | 0.493 | 0.500 | 0.498 |
| 5 | 0.519 | 0.500 | 0.497 |
| 40 | 0.535 | 0.500 | 0.496 |
| 200 | **0.540** | 0.500 | 0.495 |

The inflation grows with the number of policies tried, and a second
independent log gives the right number back. This is the same effect as
tuning hyperparameters on the reporting set, and it weighs more here because
in the offline setting no new experiments can be run at all.

## What would fix it

Report how many policies were tried, measure on a second log that played no
part in the selection, and report the probability ratios, because an estimate
resting on a handful of logged cases is unusable however unbiased it is.
