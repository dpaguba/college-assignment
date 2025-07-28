# The transient phase

A simulation usually starts empty, which is not a state the system spends
much time in. The early observations are biased downwards for a queue, and
averaging them into the result biases the answer.

The module detects the end of the warm-up by smoothing the trace and taking
the first point at which it stops trending, which is Welch's method in its
simplest form, and it shows that dropping the warm-up moves the estimate
towards the analytical value.

Detecting it is a judgement rather than a computation. The rule has no
guarantee attached, which is why the lecture treats the warm-up length as a
modelling decision to be justified rather than a number to be produced.
