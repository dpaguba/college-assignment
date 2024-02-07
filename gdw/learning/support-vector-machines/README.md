# Support vector machines

Many lines separate a separable set; the machine takes the one furthest from
the nearest points. Only those nearest points matter, which the module checks
by adding a point far from the boundary and confirming the model barely
moves.

Two things happen when the data is not separable.

**Slack.** No line exists, so the hard formulation has no solution at all and
the module returns nothing. Allowing a penalty per violated point gives a
line again, and the penalty is the parameter that trades errors against
margin.

**Kernels.** Points inside a circle cannot be separated from points outside
it by a line, and in the space of squared coordinates they can, because the
circle becomes a half plane. That is the kernel trick in its smallest form:
the boundary is linear in a space where the data is not.
