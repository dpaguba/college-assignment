# Calibration

A calibrated model says: of the cases I give seventy per cent, seventy per
cent come true. Binning the predictions checks exactly that sentence.

## Accuracy does not see it

Sharpening the probabilities towards the extremes without changing their
order:

| | before | after |
|---|---:|---:|
| expected calibration error | 0.0077 | **0.1437** |
| accuracy | 0.7477 | **0.7477** |

Every decision is the same, so the accuracy is identical to the last digit,
and the reported numbers are now wrong by a factor. That is why calibration
needs its own measurement.

## The Brier score decomposes exactly

Mean squared error of the probabilities = reliability − resolution +
uncertainty. On the example: 0.0000238 − 0.0835 + 0.2500 = 0.16654, against a
measured Brier score of 0.16654. The identity holds to machine precision and
is the check on the whole computation.

## One parameter repairs it

| | |
|---|---:|
| error before | 0.1435 |
| error after temperature 2.95 | **0.0088** |
| accuracy before and after | 0.7489 |

The transform is strictly increasing, so the accuracy cannot change. That is
the practical point: calibration is repairable after the fact, sharpness is
not.

## What calibration is not

A model that gives every case the base rate is perfectly calibrated and
useless. A model that separates perfectly can be arbitrarily miscalibrated.
Both properties are needed and both are measured separately.
