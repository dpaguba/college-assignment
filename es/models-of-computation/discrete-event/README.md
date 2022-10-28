# Discrete event models

Events carry a time stamp and are processed in time order, so the simulation
jumps from event to event and the clock is data rather than a loop counter.

Two details decide whether a model is well behaved. Simultaneous events need
a tie-breaking rule, and here it is the insertion order, because otherwise
the result depends on the internals of the queue. And an event that schedules
another with zero delay never lets the clock advance, which is Zeno behaviour
and the discrete event version of an infinite loop. The module raises rather
than running forever.

The model is what almost every simulator uses, from circuits to networks, and
its weakness is the same in all of them: the semantics of simultaneity is a
choice, and two simulators making different choices produce different
results for the same model.
