# The limits of the thread model

Threads over shared memory are the default and the lecture spends a session
on why embedded systems reach for something else.

**The result is not determined by the program.** Two threads incrementing a
shared counter give 1 or 2 depending on the interleaving, and the module
enumerates the orders to show both. A dataflow version of the same
computation has one outcome, because there is no shared cell to race over.

**Time is not in the model.** Mutual exclusion and ordering can be stated;
a deadline, a period or a jitter bound cannot, because nothing in the model
refers to time at all. A real-time requirement therefore lives outside the
program, in a scheduler configuration, and cannot be checked against the
code.

Those two gaps are the reason the rest of this block exists. Every model here
closes one of them: dataflow removes the interleaving, and the timed models
of the evaluation block put time into the specification.
