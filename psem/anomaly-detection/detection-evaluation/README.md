# Scoring a detector

The detector that never raises an alarm reaches 99.9 % accuracy at a base rate
of one in a thousand and finds nothing. Every accuracy figure has to be held
against that number.

## What the base rate does

At a base rate of 0.1 %, a detector with 99 % recall and a 1 % false alarm rate
produces, per hundred thousand cases, 99 true alarms and 999 false ones. One
in eleven alarms is real.

Turned around: for half the alarms to be real, the false alarm rate has to fall
to 0.099 %, about ten times stricter than the 1 % that reads as a good number
in a report.

## Which numbers to use

Not accuracy over all cases, which is decided by the majority. Recall,
precision, and the count of false alarms per true one. And when a curve is
drawn, precision against recall rather than against the false alarm rate: the
latter is divided by the large number of negatives and therefore always looks
small.
