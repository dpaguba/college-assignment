# Fitting a distribution

The coefficient of variation points at the family before any fitting starts:

| coefficient | family |
|---|---|
| 1 | exponential |
| below 1 | Erlang |
| above 1 | hyperexponential |

An exponential sample gives 1.00 and a nearly constant one gives 0.02, so the
statistic separates the cases the lecture cares about. The parameters then
come from matching moments, which is exact for these families and needs no
search.

The choice of family matters more than the fit within it. A queue driven by
an exponential service time behaves differently from one driven by a constant
of the same mean, and no amount of fitting inside the wrong family repairs
that.
