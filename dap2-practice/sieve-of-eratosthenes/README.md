# Sieve of Eratosthenes

Count the primes in [2, n], print them on request. Practical sheet 1, task 1.2.

```
java Eratosthenes 10 -o
4
2 3 5 7
```

## How it works

Mark everything as prime, then walk upwards striking out the multiples of each
number still marked.

Two details carry the running time. The outer loop stops at √n, because a
composite has a factor no larger than its square root and was struck out
earlier. The inner loop starts at i² rather than 2i, because every smaller
multiple of i has a smaller prime factor.

O(n log log n): each prime p strikes out about n/p numbers, and the sum of 1/p
over the primes below n grows like log log n. That is Mertens' theorem, and it
is why the sieve is so close to linear.

## Verification

Both sample calls, and all the error cases including the addendum: the order of
the parameters is fixed, and a second parameter other than `-o` is ignored
rather than rejected.

Beyond the sheet, every sieve up to n = 2000 was compared entry by entry with
`BigInteger.isProbablePrime`, and π(10⁶) came out as 78498, the known value.
