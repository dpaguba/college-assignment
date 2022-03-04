# Fixed points

Tarski's theorem: a monotone map on a complete lattice has a least and a
greatest fixed point, and both are given without any iteration. The least is
the infimum of the elements the map sends downwards, and that infimum turns
out to be a fixed point itself.

## Two ways to the same point

| | |
|---|---|
| Tarski | the infimum of the pre-fixed points, in one step |
| Kleene | iterate the map from the bottom until it stops changing |

On the subsets of a four-element set, the iteration reaches the least fixed
point in 4 steps, against a lattice height of 5. That bound is the general
statement: the ascent is strictly increasing, so it cannot be longer than the
longest chain, and on a finite lattice it always terminates.

The two constructions differ on infinite lattices, where the iteration needs
the map to be continuous and not merely monotone. The finite case hides that
distinction, which is exactly why a data flow analysis over a finite lattice
can be computed by iterating and one over an infinite one cannot.

## Monotone is required, not optional

The map sending a subset to its complement has no fixed point at all, and it
is not monotone. Tarski's theorem does not apply, and the module reports the
empty list of fixed points rather than failing, which is the useful behaviour
when the hypothesis is what is in doubt.
