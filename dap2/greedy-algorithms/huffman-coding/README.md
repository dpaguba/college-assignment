# Huffman coding

Variable-length codes that are provably the best possible.

| | |
|---|---|
| Time | O(n log n) |
| Space | O(n) |
| Greedy rule | merge the two least frequent |

## The idea

A fixed-width encoding spends the same number of bits on every symbol, which
wastes space when frequencies are uneven. Huffman gives common symbols short
codes and rare ones long codes.

Put every symbol in a min-heap keyed on frequency. Repeatedly pop the two
**least** frequent, merge them into one node whose frequency is their sum, and
push it back. The tree left at the end assigns each symbol the code spelled by
the path to its leaf.

On `"this is an example of a huffman tree"`: 16 distinct symbols need 5 bits
each fixed-width, so 180 bits; Huffman uses 135, and the space character gets
the 3-bit code `111`.

## Prefix-free

Symbols sit only at leaves, so no code is a prefix of another. That is what
makes the bit stream decodable with no separators and no lookahead: read bits
until the accumulated string is a code, emit that symbol, start over. There is
never a choice to make.

## The proof

Two lemmas.

**The two rarest symbols can be siblings at maximum depth.** In any optimal
tree, if a deeper leaf held a more frequent symbol than a shallower one,
swapping them would reduce the total. So an optimal tree exists in which the
two least frequent symbols are the deepest pair.

**Merging is safe.** Replacing that pair with a single symbol of their combined
frequency reduces the alphabet by one, and the cost of any tree for the smaller
alphabet differs from the cost of the corresponding tree for the larger one by
the same constant. So an optimal tree for the smaller problem extends to an
optimal tree for the larger.

Induction on the two gives optimality among all prefix-free codes. Huffman
proved this in 1952, as a student, in place of a final exam.

## What is worth noticing

Most greedy algorithms are heuristics that happen to be optimal on a
restricted problem. This one is optimal on the general problem, which is rare.

Its limit is the whole-bit constraint. A symbol with probability 0.9 deserves
about 0.15 bits and Huffman must spend 1. Arithmetic coding drops the
requirement that a symbol occupy an integer number of bits and approaches the
entropy bound, which is the only way to beat Huffman at its own problem.

The heap entries carry a tie-breaking counter so that comparisons never reach
the symbols themselves. Without it, Python would try to order the payloads and
the result would depend on their types.
