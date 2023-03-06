# The normal distribution

Everything reduces to the standard case by subtracting the mean and dividing
by the standard deviation, which is why one table suffices for every normal
variable.

| | |
|---|---|
| within one standard deviation | 0.6827 |
| within two | 0.9545 |
| within three | 0.9973 |

The quantiles the rest of the course uses come out of the same computation:
1.959964 at 97.5 percent and 1.644854 at 95 percent, both matching the
published tables to five decimals.

## No closed form

The distribution function has no elementary antiderivative, so it is computed
from the error function, and the quantile by inverting that numerically. The
tests check the inversion at several points, since a quantile function that
is not the inverse of its own distribution function is the kind of error that
stays hidden until a confidence interval is slightly wrong.

The three-sigma rule is worth stating precisely, because it is usually quoted
as "almost all". Two standard deviations leave 4.55 percent outside, which is
one observation in 22, and that is not rare in any sample worth analysing.
