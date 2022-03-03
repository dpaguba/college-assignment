# Boolean lattices

Distributive and complemented, which turns out to be a strong pair of
conditions: every finite Boolean lattice is the power set of its atoms.

The divisor lattice makes the condition sharp:

| number | lattice | Boolean |
|---|---|---|
| 30 = 2·3·5 | eight divisors | yes |
| 12 = 2²·3 | six divisors | no |

A squarefree number gives a Boolean lattice, because each prime is present or
absent and nothing else. One square factor breaks it: the divisors 1, 2, 4
form a chain, and 2 has no complement, since nothing meets it in 1 and joins
it to 12.

## The representation theorem, checked

The map sending each element to the set of atoms below it is a bijection onto
the subsets of the atoms, and it preserves both operations. Verified here for
the divisors of 30, which has three atoms and eight elements: 8 = 2³, as the
theorem requires.

The consequence is that a finite Boolean lattice has a power of two elements,
so there is no Boolean lattice with six or with twelve, however one arranges
them.
