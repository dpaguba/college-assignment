# Convergence

The power iteration converges geometrically, and the rate is the damping
factor: the error is multiplied by roughly 0.85 at every step, so about fifty
steps take it below one part in a hundred million.

A smaller damping factor converges faster, which the module measures. That is
the tension in choosing it: 0.85 describes a surfer who follows about six
links before jumping, and a smaller value converges quicker while describing
a surfer nobody recognises.

The error trace falls geometrically at every step, which is what the module
checks, and it is the property that makes the iteration a practical algorithm
on a graph too large to solve exactly.
