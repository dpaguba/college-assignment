# Set operations

Union, intersection, difference, complement, power set, product, and the laws
checked by enumeration.

A law about sets is a claim about every pair of subsets. Over a universe of
six elements there are 64 subsets and 4096 pairs, so De Morgan's laws are
verified exhaustively for that universe. That is a proof for the case checked
and an experiment for the general claim, and the distinction is worth keeping
in view: the enumeration cannot prove the law, and it would immediately refute
a false one.

## Inclusion and exclusion

Adding the sizes of three sets counts every element once for each set it
belongs to. Subtracting the pairwise intersections removes the overcount and
takes the triples out too often, so they are added back. The alternating sum
is checked against the size of the union, over the same sets.

## The power set is where the sizes come from

The power set of a set of n elements has 2^n members, which is the reason a
subset can be described by a string of n bits, and the reason the enumeration
above is 4096 pairs rather than something unbounded. The same count reappears
in the order chapter, where the power set ordered by inclusion turns out to be
the standard example of a Boolean lattice.
