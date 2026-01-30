# Expected improvement

The gain over the best value seen so far, in expectation over the predicted
distribution. The closed form has two terms: the mean's lead weighted by the
probability of an improvement, and the deviation weighted by the density at
the threshold.

The first term pulls towards what looks good, the second towards what is
unknown. Both are in one formula and nothing balances them by hand.

Checked against Monte Carlo integration over 400 000 draws, agreeing to two
decimals at every combination tested.

## What it chooses

| | prediction | deviation | expected improvement |
|---|---:|---:|---:|
| the safe point | 1.00 | 0.05 | 0.100 |
| the unknown point | 0.80 | 1.00 | **0.351** |

The unknown point wins although its prediction is worse. A search following
the mean alone would take the safe point, measure it, have its prediction
confirmed, and stay there forever.

## The one knob

| tradeoff | value |
|---:|---:|
| 0.00 | 0.399 |
| 0.50 | 0.198 |
| 2.00 | 0.009 |

It demands a minimum lead before a point counts at all, which makes the search
more cautious. It is almost always set to zero, which is a decision that is
rarely stated as one.
