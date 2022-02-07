# Exponential and ternary search

Find the largest array insertion sort can handle in x steps. Practical sheet 3,
task 3.2.

```
java Search 1337
links: T(16) = 435, rechts: T(32) = 1643
links: T(26) = 1100, rechts: T(32) = 1643
links: T(28) = 1269, rechts: T(30) = 1450
links: T(28) = 1269, rechts: T(29) = 1358
Ergebnis: T(28) = 1269
```

## The idea

T(n) = (3n² + 7n − 10)/2 is insertion sort's worst case from the lecture. The
question is the largest n with T(n) ≤ x, and it could be answered by inverting
the inequality. It is answered by searching instead.

That is the useful half of the exercise: the search needs nothing but the
ability to evaluate T, so it also works for functions with no closed-form
inverse. All it needs is monotonicity.

## Two phases

**Exponential search** doubles m from 1 until T(m) > x, which brackets the
answer in O(log n) evaluations without knowing any bound in advance. This is
the standard way to turn an unbounded search into a bounded one: binary search
needs a right end, and doubling manufactures one.

**Ternary search** then narrows [ℓ, r) by probing at one third and two thirds.
It cuts two thirds per round, so log₃ rounds, but two evaluations per round
instead of one: 2/log₂3 ≈ 1.26 times as many evaluations as binary search. On a
monotone function ternary search is a demonstration, not an improvement. It
earns its place on unimodal functions, where a single midpoint tells you
nothing.

## long, not int

x may be large enough that n reaches the millions, and n² leaves the int range
long before T does anything interesting. For x = 10⁹ the answer is n = 25818,
which the closed form ⌊(√(24x + 169) − 7)/6⌋ confirms.

## Verification

Both traces from the sheet, line for line, and the error case.
