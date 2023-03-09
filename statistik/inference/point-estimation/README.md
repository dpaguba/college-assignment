# Point estimation

An estimator is a random variable, so it has a distribution of its own. It is
unbiased when its expectation is the parameter, and the sample variance is
the standard example of what goes wrong.

Measured on samples of four from the modified die, over 40 000 repetitions:

| estimator | bias |
|---|---:|
| variance with the correction | -0.003 |
| variance without it | -0.565 |
| the theoretical shortfall, Var/n | -0.5625 |

The uncorrected estimator is low by very nearly a quarter of the variance,
which is exactly what the theory predicts for n = 4. The correction is not a
convention: the deviations are measured from the sample mean, which sits
closer to the data than the true mean does, so without dividing by n-1 the
estimate is systematically too small.

## The error decomposes

The mean squared error of an estimator is its squared bias plus its variance,
verified numerically here. That is the reason a biased estimator is sometimes
preferred: trading a little bias for a large reduction in variance can lower
the total error, which is the same trade that appears in machine learning
under the same name.
