# Euclid

Greatest common divisor of two positive integers. Practical sheet 1, task 1.1.

```
java Euclid 264 846
6
```

## The algorithm

`gcd(a, b) = gcd(b, a mod b)`, and `gcd(a, 0) = a`. It works because any common
divisor of a and b also divides a − qb, and conversely, so the pair keeps its
divisors while the numbers shrink.

O(log min(a, b)) divisions. The worst case is a pair of consecutive Fibonacci
numbers, which is Lamé's theorem from 1844 and the first running-time analysis
of an algorithm ever written down.

The arguments do not need to be ordered: if a < b, the first step swaps them,
because a mod b = a in that case.

## Verification

Both sample calls from the sheet and all four error cases, including the
addendum of 29 April that restricts the input to natural numbers greater than
zero.
