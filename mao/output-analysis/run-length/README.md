# Run length

Precision is bought by the square: halving the half width needs four times
the observations, which the module checks.

The practical answer is sequential. Run until the interval is small enough
rather than deciding the length in advance, because the variance is not known
before the run and a length chosen from a guess is either wasteful or
insufficient.

The cost depends on the system as well as on the target. A queue at 90
percent load needs far more replications for the same precision than one at
50 percent, because its response time varies far more, so a study of a
congested system is expensive exactly where the answer matters most.
