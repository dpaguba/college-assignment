# Sums of random variables

Expectations always add. Variances add only when the variables are
uncorrelated:

```
Var(X + Y) = Var(X) + Var(Y) + 2 Cov(X, Y)
```

The module includes a pair where that matters. Two variables that always sum
to one have positive variance each and a constant sum, so the variance of the
sum is zero and the covariance term closes the whole gap. The tests check the
identity numerically rather than the special case, so the general rule is the
thing being verified.

## Convolution

The distribution of a sum of two independent variables is the convolution of
their distributions. Two fair dice give the familiar triangle with 7 at
probability 6/36, and two binomials with the same success chance add to a
binomial with the trials added, checked term by term.

That additivity is what makes the binomial the distribution of a count: the
count of successes in n trials is a sum of n indicators, and the expectation
and variance of the binomial follow from the rules above without any
computation with factorials.
