# Bias and variance

The expected error splits into three terms, measured here by fitting
polynomials to two hundred samples of a noisy quadratic:

| degree | bias² | variance | total error |
|---|---:|---:|---:|
| 0 | 0.107 | 0.021 | 0.218 |
| 1 | 0.003 | 0.040 | 0.133 |
| 3 | 0.000 | 0.031 | 0.122 |
| 9 | 168 | 29 145 | 29 313 |

The constant model has the highest bias and the lowest variance. The degree
nine polynomial has no bias at all and a variance of 29 145, which is not a
typographical error: with twelve noisy points a nine degree fit passes close
to all of them and its prediction at a fixed point swings wildly between
training sets.

The noise term is 0.09 in every row and no model removes it. The total has a
minimum in the middle, and finding it is what model selection is.
