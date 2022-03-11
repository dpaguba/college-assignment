# Order structures

| Topic | |
|---|---|
| [partial-orders](partial-orders/) | diagrams, chains, antichains, linear extensions |
| [lattices](lattices/) | two bounds, four laws, two counterexamples |
| [complete-lattices](complete-lattices/) | every subset, including the empty one |
| [boolean-lattices](boolean-lattices/) | complemented and distributive, hence a power set |
| [fixed-points](fixed-points/) | Tarski and Kleene, and where they differ |
| [order-homomorphisms](order-homomorphisms/) | monotone against structure preserving |

The first half of the second part of the lecture. An order becomes a lattice
when every pair has both bounds, a complete lattice when every subset does,
and a Boolean lattice when it is also distributive and complemented. Each
condition is checked here by enumeration, and each has a smallest
counterexample that the tests use.

The result the rest of computer science borrows is Tarski's theorem. Every
monotone map on a complete lattice has a least fixed point, and on a finite
lattice the iteration from the bottom reaches it in at most the height of the
lattice, which is 4 steps out of a possible 5 in the example here. That is
the justification for computing a data flow analysis by iterating until
nothing changes.
