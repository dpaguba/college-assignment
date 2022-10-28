# Kahn process networks

Processes, unbounded channels, and blocking reads. One prohibition carries
the whole model: a process may not test whether a channel is empty.

With that rule the network is deterministic. The output depends on the inputs
and not on the relative speed of anything, so a network can be run in any
order and gives the same answer, which the module checks by running one in
six different orders.

Allowing the test breaks determinism immediately. The peeking network in the
module gives different results depending on how far ahead the producer has
run, and nothing in the program says which is right.

Two things are given up for that guarantee. The channels are unbounded, so an
implementation with finite buffers can deadlock where the model does not, and
a process cannot react to the absence of data, which rules out timeouts. The
synchronous dataflow of the previous module is the special case that trades
generality for a compile time schedule.
