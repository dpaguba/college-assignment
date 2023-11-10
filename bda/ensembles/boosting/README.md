# AdaBoost

Each round fits a classifier to weighted data, gives it a weight of the log
odds of being right, and multiplies the weights of the points it got wrong so
the next round concentrates on them.

The tenth exercise sheet works through two rounds and the module reproduces
it exactly:

| | published | computed |
|---|---|---|
| ε₁ | 0.3 | 0.3 |
| α₁ | ln(7/3) | 0.8473 |
| weights after round 1 | 1/6 and 1/14 | 1/6 and 1/14 |
| ε₂ | ≈ 0.286 | 0.2857 |
| α₂ | ≈ 0.916 | 0.9163 |

## Why "better than chance" is the only requirement

The classifier weight is the log odds of being right, so it is positive below
an error of one half, zero at exactly one half, and negative above it. A
learner worse than chance enters the ensemble inverted and still helps, and a
learner at exactly one half contributes nothing at all. Both cases are in the
module.
