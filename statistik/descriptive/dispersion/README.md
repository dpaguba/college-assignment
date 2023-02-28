# Dispersion

For metric data the variance, for categories an index. The first sheet
computes both for the beer example, 40 Üttinger, 60 Kormbacher, 20 Fitburger:

| | |
|---|---|
| Simpson's D | 0.611 |
| normalised | 0.9165 (published), 0.9167 (exact) |
| Leti's D | 0.361 |
| normalised | 0.722 |

Simpson's index is the chance that two draws land in different categories. It
uses only the shares, so it says nothing about which categories are close to
each other. Leti's index reads the cumulative distribution and therefore
notices the order, which is why an ordinal variable gets a different number
from the two, and why the beers had to be sorted by price before the second
could be computed.

## Where the published number differs

The solution rounds the index to 0.611 before multiplying by 1.5 and prints
0.9165. Multiplying first gives 0.9167. The module reproduces both, and the
difference is the reason it takes a rounding argument at all: the published
number cannot be reached by exact arithmetic, only by rounding in the same
place.

## Variance

The exam data has variance 0.944 with the correction for a sample and 0.85
without it. The correction is not cosmetic: the deviations are measured from
the sample mean, which sits closer to the data than the true mean does, so
the uncorrected estimate is systematically too small. The size of that effect
is measured in [point-estimation](../../inference/point-estimation/).
