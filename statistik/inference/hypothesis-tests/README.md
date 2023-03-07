# Hypothesis tests

A test is a decision rule, so its result is a random variable and it can be
wrong in two ways. The level fixes how often it rejects a true hypothesis;
the power is how often it rejects a false one.

Measured over 2000 to 3000 simulated samples:

| | |
|---|---|
| rejections when the hypothesis is true, at level 0.05 | 0.05 |
| power at a distance of 0.2 standard deviations, n = 30 | low |
| power at a distance of 1.0, n = 30 | high |
| power at level 0.01 against level 0.10, same distance | lower |

The last row is the trade the chapter is about: a stricter level rejects less
often when it should not and also less often when it should. Nothing removes
that tension except more data.

## Three tests, three assumptions

**The mean test** compares the standardised distance from the hypothesised
mean with a normal quantile. It assumes enough data for the normal
approximation.

**The chi-square test of independence** compares the association statistic
with a chi-square quantile, computed here through the regularised incomplete
gamma function. Numerical integration fails for one degree of freedom, where
the density has a pole at zero: a midpoint rule reports 0.9425 at the point
where the true value is 0.95, and the critical value then comes back
unbounded. The quantiles now match the published tables to four decimals.

**The sign test** counts observations above the hypothesised median and
compares that count with a binomial distribution. It assumes nothing about
the shape at all, which is why an outlier of 50 in a sample of five does not
move it, and why it cannot reject at the five percent level with five
observations: the smallest attainable two-sided p value is 0.0625.
