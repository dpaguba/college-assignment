# Measuring when the case is rare

## Two measures with different zero points

A detector with no information at all, on a 1 % rate:

| | |
|---|---:|
| area under the ROC curve | 0.484 |
| average precision | **0.0094** |

The area sits at one half whatever the rate is. The average precision sits at
the rate itself, so it has no fixed zero point and a value of 0.05 can be
excellent or worthless depending on how rare the case is.

## The same detector, two rates

| | 10 % positives | 1 % positives |
|---|---:|---:|
| area under the ROC curve | 0.918 | **0.924** |
| average precision | 0.660 | **0.291** |

The area does not move because it normalises the two classes separately. The
average precision more than halves. Reporting only the first hides the
property of the task that matters most to whoever has to act on the alarms.

## Point adjustment, and what it does to a random detector

The common evaluation for time series counts a whole anomalous segment as
found if any point inside it was flagged. With ten segments of twenty points:

| detector | F1 plain | F1 after adjusting |
|---|---:|---:|
| a weak but real one | 0.79 | 1.00 |
| **flagging at random** | **0.045** | **0.499** |

A detector that flags 5 % of all points uniformly at random goes from
worthless to something that would pass as a result. One hit explains twenty
points, and with twenty points per segment a random detector hits most
segments.

## What belongs in a report

The rate of real cases, both measures, and the evaluation protocol. Without
the rate the average precision cannot be placed; without the protocol the
numbers are not comparable at all.
