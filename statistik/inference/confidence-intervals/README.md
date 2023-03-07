# Confidence intervals

A 95 percent interval does not say the parameter lies inside it with
probability 0.95. The parameter is fixed and the interval is random. What the
level promises is that intervals built this way cover the parameter in 95
percent of samples, which is a statement about the procedure and can
therefore be measured.

Measured on the modified die, over 3000 samples each:

| sample size | coverage |
|---|---:|
| 5 | 0.914 |
| 10 | 0.910 |
| 30 | 0.936 |
| 100 | 0.945 |

The nominal level is 0.95 and the small samples fall short by about four
points. That is the price of using a normal quantile where the exact
distribution of the standardised sample mean is a t distribution with heavier
tails, and it is a measurement of exactly how much the approximation costs.

## Width

The width is proportional to the quantile and to one over the square root of
the sample size, so quadrupling the sample halves the interval, and the tests
check that ratio. Buying precision is expensive in a way the square root
makes concrete: one more decimal costs a hundred times the data.
