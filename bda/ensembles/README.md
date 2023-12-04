# Ensembles

| Topic | |
|---|---|
| [bagging](bagging/) | averaging away the variance |
| [boosting](boosting/) | reweighting towards the mistakes |
| [random-forests](random-forests/) | both, plus decorrelation |

Chapter five's second half, and the block with the sharpest published
oracle: the tenth sheet's AdaBoost rounds come out exactly, from ε₁ = 0.3
and α₁ = ln(7/3) through the weights of 1/6 and 1/14 to ε₂ = 0.286.

The two methods attack different terms. Bagging lowers the variance and
leaves the bias, so it needs an unstable base learner. Boosting lowers the
bias by fitting the residual errors, so it works with a learner that is
barely better than chance and would overfit given a strong one.
