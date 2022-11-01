# Design space exploration

Enumerate the configurations, remove the infeasible ones, keep the front.

The space is a product of parameter choices, so it grows quickly and most of
it is discarded twice: once by the constraints, which remove what cannot be
built, and once by domination, which removes what nobody would choose. What
remains is the set a designer actually has to decide between.

The module builds a small space from frequencies and memory sizes, computes
energy and time for each, and shows both filters shrinking it. The front is
always smaller than the space and never empty, which are the two properties
that make the method worth running.
