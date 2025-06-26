# Component model

A series is read as trend plus season plus residual. The trend comes from a
centred moving average over one full season, with half weights at the two
ends so the window stays symmetric; the seasonal figure is the mean deviation
from the trend at each position within the season, shifted to sum to zero;
the residual is what is left.

## Checked against a known answer

The example series is built from a known trend (10 + 0.05 t) and a known
season (3 sin) plus a small disturbance. The decomposition recovers the trend
to within 0.020 and the seasonal figure to within 0.020. The three components
add back up to the original series exactly wherever the trend is defined.

The moving average has no value for the first and last half-season: there is
no full window there, and inventing one would invent a trend.

## Additive or multiplicative

On a series whose seasonal swing grows with its level, the multiplicative
model, which divides where the additive subtracts, gives a mean squared
residual of 0.0003 against 0.53. Which model to use is a question about the
data, and the residual answers it.
