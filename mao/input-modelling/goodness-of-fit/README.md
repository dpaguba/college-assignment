# Goodness of fit

The Kolmogorov-Smirnov statistic is the largest vertical distance between the
empirical distribution function and the fitted one. It uses every
observation, needs no buckets, and the module returns the distance as well as
the probability, because the distance is the interpretable number.

A sample from the hypothesised distribution is not rejected and a sample from
another one is, which is the minimum a test has to do and is worth checking
on a test one has just implemented.

The chi-square variant needs buckets and enough observations in each, and the
module refuses rather than producing a number from three points. That refusal
is the useful behaviour: a test statistic computed from too little data is
not a weak result, it is not a result.

With enough data every fitted distribution is eventually rejected, because no
family is exactly right. That is why the lecture treats fitting as a
modelling decision to be justified rather than a hypothesis to be tested.
