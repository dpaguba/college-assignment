# Relations between processes

Three ways two processes can be related:

- **Sequence:** one follows the other. A horizontal relation.
- **Decomposition:** one is part of the other. Vertical.
- **Specialisation:** one is a variant of the other. Also vertical, and the
  one that gets confused with decomposition.

The test that separates the two vertical relations: ask whether both run in
the same case. The parts of a decomposition all run and together make up the
whole; of two variants exactly one runs.

`Produkte vermarkten (DE)` and `Produkte vermarkten (US)` are variants of
`Produkte vermarkten`. `Einzelteile montieren` is a part of
`Produkte herstellen`. `Produkte liefern` follows it.

## What the code adds

`check_hierarchy` reads a decomposition as a set of edges and refuses a
cycle. A process cannot be an indirect part of itself: the levels of the
architecture would no longer be numberable, and the map could not be drawn.
The same walk returns the depth, the roots and the leaves, which is what the
three-level architecture needs.
