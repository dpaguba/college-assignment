# Cycle time efficiency

CTE = theoretical cycle time / cycle time. The share of the elapsed time in
which somebody is actually working on the case.

The unit trap comes first: the exercise gives cycle times in days and
processing times in hours, and a working day has eight hours. `report`
converts before dividing, and `efficiency` refuses a value above one, which
is the shape the mistake takes when the conversion is forgotten.

## The two exercises

| Process | Work | Elapsed | CTE |
|---|---:|---:|---:|
| Exposé | 28.5 h | 68 h | 41.9 % |
| Loan application with rework | 8.9 h | 69.2 h | 12.9 % |

Forty-two percent is high for an administrative process. Thirteen percent is
the normal one: the case spends seven eighths of its life in a queue.

## What the number is for

It says where to look. At 12.9 %, halving the time of an activity buys about
a sixteenth of the cycle time, and there is a factor of seven sitting in the
handovers. The instinct to make the work faster is the wrong instinct here,
and the number is what says so before anybody spends a quarter on it.
