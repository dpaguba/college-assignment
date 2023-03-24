# Wahrscheinlichkeitsrechnung und Mathematische Statistik

Twenty-seven modules in seven blocks, following the ten chapters of the
lecture. The course publishes worked solutions to all seven exercise sheets,
so most of this is checked against them directly.

| Block | |
|---|---|
| [descriptive](descriptive/) | scales, location, dispersion, quantiles, grouped data |
| [bivariate](bivariate/) | contingency tables, association, correlation, regression |
| [probability](probability/) | spaces, conditioning, independence, counting |
| [random-variables](random-variables/) | distributions, moments, transformations |
| [distributions](distributions/) | the standard families and the limit theorems |
| [multivariate](multivariate/) | joint distributions, covariance, sums |
| [inference](inference/) | estimation, likelihood, intervals, tests |

## The published solutions, reproduced

| Sheet | Reproduced |
|---|---|
| 1 | n = 10, mode 2, median 2, mean 2.5, quartiles 2 and 3; Simpson 0.611 and 0.9165; Leti 0.361 and 0.722 |
| 2 | histogram heights 0.01 to 0.048, median class (165, 170]; the pizza table with margins 110, 100, 130 and both conditional distributions |
| 3 | chi-square 33.191, corrected coefficient 0.366; covariance 14, correlation 0.904, regression 103.5 + 3.5·age |
| 5 | the modified die: expectation 3.5, variance 2.25 |
| 7 | total probability 0.62, Bayes 0.097; the maximum likelihood estimator of the normal standard deviation |

## Reproducing a published number means reproducing its rounding

Several published values cannot be reached by exact arithmetic. The solution
rounds to three decimals and continues from the rounded figures, so it prints
0.9165 where the exact answer is 0.9167, 33.191 where it is 33.1924, and
0.383 where it is 0.382. The rounded conditional rows no longer sum to one:
Italy's comes to 1.0034.

The modules compute both paths and the tests check both. That is the only way
to reproduce a published table and still know what the exact figures are.

## Numbers worth keeping

| | |
|---|---:|
| bias of the uncorrected variance at n = 4 | -0.565, theory -0.5625 |
| coverage of a nominal 95% interval, n = 10 | 0.910 |
| the same at n = 100 | 0.945 |
| central limit distance, 1 against 40 summands | 0.203 against 0.034 |
| Chebyshev at two deviations against the normal | 0.250 against 0.046 |
| binomial to Poisson at n = 1000, p = 0.002 | error 0.00018 |
| hypergeometric to binomial at N = 100 000 | error 0.00001 |
| smallest two-sided p value of a sign test with n = 5 | 0.0625 |

## Three results that argue with the first guess

**The confidence level is not what a small sample delivers.** An interval
built with the normal quantile 1.96 covers the mean in 91 percent of samples
of ten, not 95. The gap is exactly what the t distribution exists to close,
and it is measurable without knowing any of that theory.

**Chebyshev's bound is loose by a factor of five.** At two standard
deviations it allows 25 percent outside where a normal distribution puts 4.6
percent. That looseness is the price of assuming nothing about the shape, and
it is why the bound proves the law of large numbers and predicts nothing
useful about a particular distribution.

**A sign test on five observations cannot reject at five percent.** Whatever
the data, the smallest attainable two-sided p value is 0.0625. A test can be
correctly implemented, correctly applied, and incapable of the answer it is
being asked for.

## Verification

scipy on this machine is compiled against an incompatible numpy and cannot
run, so the distributions are checked against published tables instead: the
normal quantiles 1.959964 and 1.644854 to five decimals, seven chi-square
quantiles to four, and every probability function summing to one to twelve.
The correlation agrees with numpy to nine decimals, and everything about
estimators, intervals and tests is measured by simulation, because those are
statements about procedures and not about numbers.
