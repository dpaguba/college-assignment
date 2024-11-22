# Overfitting

| degree | training error | test error |
|---:|---:|---:|
| 0 | 0.390 | 0.812 |
| 3 | 0.053 | 0.129 |
| **5** | 0.040 | **0.059** |
| 8 | 0.035 | 0.162 |
| 11 | 0.030 | 0.665 |

The training error falls with every degree, and it must: a polynomial of
degree d is also one of degree d+1 with a zero coefficient, so the best fit
cannot get worse. The test error has no such argument and turns back up.

## The extreme case

Eight points, degree seven: the polynomial passes through every point.

| | |
|---|---:|
| training error | 4.7 × 10⁻²⁶ |
| test error | **8 521** |

Zero training error says nothing at all here. The model has memorised the
data, noise included.

## More data move the turning point

With 20 points the best degree is 5; with 200 it is 7. An extra degree of
freedom costs less variance when there are more points to pin it down. That is
the whole relationship between model complexity and sample size, and it is
also why the project's advice to generate as much training data as possible is
not just about compute time.

## When to stop

The slide says it plainly in passing: we stop when we have the desired result.
That is the most accurate description of practice and the most dangerous rule
in it. Compare enough models and one of them will look good on any test set;
the test error then becomes the training error of a second, invisible fit. The
only defence is a third set that gets used once.
