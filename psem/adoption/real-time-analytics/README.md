# Real-time analytics

Three classes by latency: batch in hours to days over all the data, micro
batch in seconds to minutes over a window, stream in milliseconds one record
at a time.

## The trade-off

Answer immediately and the answer is incomplete, because what is still in
flight is missing. Wait until everything has arrived and the answer is late.
There is no free middle: the decision is how much incompleteness the answer
tolerates. With late arrivals a further question follows, namely whether an
answer already given can be withdrawn.

## The overlapping window trap

With a window of ten seconds sliding every five, each record falls into two
windows. Summing over the windows therefore counts every record twice. It is
the same trap as a non-additive measure in a cube, moved from a dimension to
time.

## Why the choice is about cost

A stream is not harder to compute than a batch; it is harder to operate. State
over time, restart after a failure, late records and exactly-once counting all
cost operations rather than processor time. That is what decides the class,
not the algorithm.
