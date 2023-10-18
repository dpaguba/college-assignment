# Expectation maximisation

k-means assigns each point to one cluster. A mixture model gives each point a
probability of belonging to each component, and the algorithm alternates
between computing those probabilities and refitting the components.

The soft assignment is the difference worth seeing. On the points 0, 2 and 4
with two components, the middle point splits exactly in half, and no hard
assignment can express that. On well separated data the responsibilities
collapse to zero and one, so the soft method contains the hard one as a
limiting case.

The likelihood never falls, which the module checks step by step. That is the
guarantee the method offers, and it says nothing about the optimum being
global: like k-means, it converges to whatever the starting point leads to.
