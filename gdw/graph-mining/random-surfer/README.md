# The random surfer

PageRank is defined as the limit of a walk, and the walk can be run. Two
hundred thousand steps on the exercise graph reproduce the computed ranks to
within two hundredths.

That agreement is the point of the module: the formula and the story are the
same object, and a simulation is the cheapest way to see it.

Teleporting is what makes the chain irreducible. With a damping factor below
one every node can be reached from every other, so the stationary
distribution is unique. At damping one, a graph with a sink is not
irreducible, and the module reports the difference rather than describing it.
