# Arrays and matrices

The second sheet, where the loop's end condition becomes part of the problem.

**Pairs of equal neighbours.** Each element belongs to at most one pair, so a
match advances the index by two and a run of four equal values gives two
pairs. The published examples are the test: `1 1 3 3 1 2 2 2 1` has three
pairs and `1 3 3 3 3 2 2 5 5` has four.

**Largest proper divisor.** Searching downwards from the value finds the
answer immediately for even numbers and runs the whole way for primes.
Searching upwards for the smallest divisor and dividing gives the same answer
after at most the square root of the value in steps, which is the version
implemented here.

**Prime factorisation.** The loop stops when the remaining value has been
reduced past the square root, and whatever is left is the last prime factor.
That final step is the one that is easy to forget and is the reason 97 comes
back as itself rather than as nothing.

**The sieve.** Marking from the square of each prime rather than from its
double is the same optimisation seen from the other side: every smaller
multiple has already been marked by a smaller prime.

**Matrices.** Row sums, column sums, transposition and symmetry. Symmetry is
the one that needs care, because a matrix that is not square cannot be
symmetric and indexing it as though it were throws instead of answering.
