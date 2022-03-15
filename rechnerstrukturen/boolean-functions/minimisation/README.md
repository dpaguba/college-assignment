# Quine and McCluskey

Two steps, and they are different problems. Finding the **prime implicants** is
mechanical: combine terms differing in one position, replacing it by a dash,
until nothing combines. Choosing a **minimal subset** covering every one-row is
set cover, which is NP-hard.

## The sheet's function

Five variables, value vector with ones at 1, 3, 5, 7, 9, 11, 13, 15, 30, 31.
The first level holds those ten minterms, and the algorithm finds **three**
prime implicants:

| implicant | covers |
|---|---|
| `!a e` | 1, 3, 5, 7, 9, 11, 13, 15 |
| `a b c d` | 30, 31 |
| `b c d e` | 15, 31 |

The third is a genuine prime implicant, since neither of the others contains
it, and it is **not essential**: the first two already cover every one-row.
The minimal cover is those two, which is what the PI table selects.

That distinction is the point of the exercise. Enumerating the primes is
mechanical and gives three; choosing among them is the part that needs the
table, and it gives two.

## Verified

Against brute force on all 256 three-variable functions: for every one, the
minimal cover computes exactly the function it was derived from.

## Literals, not terms

A cover's cost is its literal count, not its term count: two terms of five
literals are larger than three terms of two. That is the measure a gate count
follows.
