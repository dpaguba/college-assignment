# Synchronous dataflow

Fixed rates per firing, and everything decidable before anything runs.

The balance equations give the repetition vector, the firing counts that
return every channel to its starting state. For the three-actor graph here it
is 3, 6 and 2, the schedule has eleven firings, and the largest buffer holds
six tokens. All three numbers come out of the graph and none of them needs an
execution.

An inconsistent graph has no repetition vector at all, and the module reports
that rather than producing a schedule that drifts.

## What the restriction buys

Data dependent rates are forbidden, and in exchange the schedule, the buffer
sizes and the absence of deadlock are all compile time properties. That is
the whole argument for the model in signal processing, where the rates really
are fixed, and the reason it is useless for general computation, where they
are not.

A cycle without initial tokens deadlocks, and one token breaks it. The module
checks both, which is the smallest example of why an initial token is a
design decision rather than an initialisation detail.
