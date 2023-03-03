# Discrete distributions

Four distributions, four different questions about the same kind of
experiment.

| | counts |
|---|---|
| binomial | successes in n independent draws with replacement |
| hypergeometric | successes in n draws without replacement |
| geometric | draws until the first success |
| Poisson | events in an interval, when they are rare and independent |

## The approximations, measured

**Hypergeometric to binomial.** Drawing 5 from a population of 100 000 with
20 percent successes gives 0.40961024, against 0.40960000 for the binomial.
Without replacement stops mattering when the population is large, because
removing one item barely changes the composition.

**Binomial to Poisson.** With 1000 trials at a chance of 0.002, the
probability of exactly 3 successes is 0.180628, against 0.180447 for the
Poisson with rate 2. The error is 0.00018, so the approximation is good to
three decimals and not to four, which is the sort of statement that needs a
measurement rather than a rule of thumb.

## Memorylessness

The geometric distribution is the only discrete distribution on the positive
integers for which having waited changes nothing about the remaining wait.
The module checks the property across a grid of waiting times rather than
citing it, and its continuous counterpart, the exponential distribution,
appears in the next module with the same check.
