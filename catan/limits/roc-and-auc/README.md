# The ROC curve and its area

Every threshold from the highest score downwards, and at each one the share of
positives and the share of negatives called positive. The area under the
resulting curve is computed three ways and the three agree to nine decimals:
by the trapezoid rule, by counting pairs, and by accumulating rectangles.

The pair count is the more meaningful definition: the area is the probability
that a randomly chosen positive scores above a randomly chosen negative, with
a tie counting as half.

## What the area does and does not measure

It measures the ranking, not the calibration. Any strictly increasing
transform of the scores leaves it unchanged, so a model whose probabilities
are wildly miscalibrated can still reach 1.0. Anyone who needs probabilities
rather than an order is reading the wrong number.

## It does not notice imbalance

The same separability, once with balanced classes and once with a twentieth as
many positives:

| | balanced | imbalanced |
|---|---:|---:|
| area under the curve | 0.932 | **0.931** |
| precision at the same operating point | 0.866 | **0.213** |

The area barely moves because it normalises the two classes separately.
Precision collapses because the false alarms are now measured against very few
positives. Both numbers are correct; they answer different questions, and it
is precision that answers the user's.

For a game AI this is the case that matters, since the moves worth singling out
are rare.
