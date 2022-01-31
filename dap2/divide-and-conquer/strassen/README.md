# Strassen matrix multiplication

Seven block products instead of eight.

| | |
|---|---|
| Time | O(n^2.807) |
| Recurrence | `T(n) = 7T(n/2) + O(n²)` |
| Master theorem | case 1, the leaves dominate |

## The idea

Splitting each matrix into four blocks turns one n×n product into eight products of
half the size, giving T(n) = 8T(n/2) + O(n²), which resolves to n³. **The recursion
by itself buys nothing.**

Strassen's 1969 discovery is a set of seven products, each a combination of block
sums, from which all four result blocks can be assembled.

## What is worth noticing

The seven combinations look arbitrary and are not derived from anything intuitive,
which is exactly why the result was a surprise: the obvious decomposition was not
the only one. It opened the search for lower exponents that is still running, with
the current record around 2.371 and none of those algorithms practical.

Strassen itself becomes worthwhile from a few hundred rows, so real libraries switch
to it above a threshold and use the plain method below. This implementation does the
same, and pads odd sizes with zeros rather than special-casing them.
