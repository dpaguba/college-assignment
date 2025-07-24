# Confidence intervals

An interval needs independent observations, and a simulation produces a
correlated series. Computing the usual interval from the raw output gives a
number that is too narrow and claims a coverage it does not have.

Two repairs. Run the model many times with different seeds, which gives one
independent observation per run, or batch a single long run, which is the
next module.

The half width falls with the square root of the number of observations, so
halving it costs four times the runs. That is the economics of the whole
subject, and the module checks the ratio rather than stating it.
