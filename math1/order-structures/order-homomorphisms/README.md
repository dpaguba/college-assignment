# Order homomorphisms

Two notions of a structure-preserving map, and the gap between them.

A **lattice homomorphism** preserves join and meet. A **monotone map**
respects the order. Every lattice homomorphism is monotone, because the order
is definable from either operation, and the converse fails.

The counterexample is found by enumeration rather than constructed by hand:
among the maps from the subsets of a two-element set to the divisors of 6,
there are maps that respect every comparison and still send a join somewhere
other than the join of the images. A monotone map can push two incomparable
elements to the same place, and their join then has nowhere to go.

## Isomorphism

An order isomorphism is a bijection whose inverse is monotone as well, which
is a stronger condition than being a monotone bijection. The subsets of a
two-element set and the divisors of 6 are isomorphic, and the subsets of a
two-element set and a four-element chain are not, although both have four
elements. The module finds the isomorphism by searching every bijection,
which is why the orders here stay small and why a negative answer means
something.
