# Distributions

| Topic | |
|---|---|
| [discrete-distributions](discrete-distributions/) | binomial, hypergeometric, Poisson, geometric |
| [continuous-distributions](continuous-distributions/) | uniform and exponential, from the definition |
| [normal-distribution](normal-distribution/) | the standard table and the quantiles |
| [limit-theorems](limit-theorems/) | why the normal distribution turns up everywhere |

Chapter eight, plus the limit theorems that justify half of the inference
block. Every distribution here is checked twice: its probabilities sum to one
to twelve decimals, and its quantiles agree with the published tables, since
scipy on this machine is built against an incompatible numpy and cannot be
used as an oracle.

The approximations are stated as measurements rather than as rules. The
binomial approaches the Poisson to within 0.00018 at 1000 trials and a chance
of 0.002; the hypergeometric approaches the binomial to within 0.00001 at a
population of 100 000; and the central limit distance falls from 0.203 to
0.034 between one summand and forty.
