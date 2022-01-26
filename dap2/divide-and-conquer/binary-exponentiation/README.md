# Binary exponentiation

A power in log n multiplications instead of n.

| | |
|---|---|
| Time | O(log n) |
| Recurrence | `T(n) = T(n/2) + O(1)` |
| Master theorem | case 2, Theta(log n) |

## The idea

Squaring doubles the exponent reached: x² gives x⁴ gives x⁸, and the binary digits
of n say which of those to keep. x^13, with 13 = 1101, is x⁸·x⁴·x¹: three squarings
and two combinations against twelve multiplications for the naive loop.

Divide and conquer in its smallest form, x^n = (x^(n/2))².

## What is worth noticing

**It never needed numbers.** The halving works for anything associative, so the same
code raises matrices, permutations and group elements. The Fibonacci matrix
[[1,1],[1,0]] raised to n holds F(n) in its corner, which computes Fibonacci in
O(log n) multiplications rather than O(n) additions.

Reducing modulo at each step keeps the numbers small, and that variant is what RSA
and Diffie-Hellman are built from: the exponent can be astronomical while the work
stays logarithmic.
