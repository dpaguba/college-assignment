# The model

Map on each input, shuffle by key, reduce on each group. The number of
reducers does not change the result, which the module checks, and it does
change how the work is spread.

The key decides the parallelism. On a thousand records sharing one key and
one record with another, one reducer receives everything and the run time is
that reducer's, whatever the cluster size. The module measures the largest
share and gets 1.0.

That skew is the failure mode of the model, and it is invisible in the
program: the code is correct, the answer is correct, and the job takes as
long as a single machine would.
