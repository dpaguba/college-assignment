# Maximum likelihood

The parameter under which the observed data was most likely. The recipe is
the same every time: write the likelihood, take the logarithm because the
likelihood is a product, differentiate, set to zero.

| model | estimator |
|---|---|
| Bernoulli | the share of successes |
| Poisson | the sample mean |
| exponential | the inverse of the sample mean |
| normal, mean known | the root mean squared deviation from the mean |

The seventh sheet asks for the last of these, and the module reproduces it.
For the sample used in the tests the answer is exactly 2.

## The estimator is not automatically unbiased

With the mean estimated from the same data, the maximum likelihood estimator
of the variance divides by n, which is exactly the biased estimator measured
in [point-estimation](../point-estimation/). Maximum likelihood optimises
the fit to the data at hand and says nothing about the expectation of the
estimator over repeated samples, and those are different criteria.

The tests check the estimate two ways: that it beats several competing
parameter values on the same data, and that it is a zero of the derivative of
the log likelihood. The first is the definition, the second is the method,
and checking both is how a sign error in the derivative gets caught.
