# Karatsuba multiplication

Multiplying two numbers with three smaller products instead of four.

| | |
|---|---|
| Time | O(n^1.585) |
| Recurrence | `T(n) = 3T(n/2) + O(n)` |
| Master theorem | case 1, the leaves dominate |

## The idea

Schoolbook multiplication of two n-digit numbers costs n² digit products, and until
1960 that was believed optimal; Kolmogorov had conjectured it. Karatsuba, then
twenty-three, disproved it in a week.

Split each number: x = a·B + b, y = c·B + d. The product needs a·c, b·d and the
cross term a·d + b·c, which looks like four multiplications. The trick:

```
a·d + b·c = (a + b)·(c + d) - a·c - b·d
```

Both a·c and b·d are already computed, so the cross term costs one more
multiplication rather than two.

## What is worth noticing

**Three instead of four** changes T(n) = 4T(n/2) + O(n), which resolves to n², into
T(n) = 3T(n/2) + O(n), which gives n^log₂3 ≈ n^1.585.

Additions grew in number, and additions are linear, so the trade stays favourable
as n grows. This was the first algorithm to beat n² for multiplication and it opened
the line running through Toom-Cook and Schönhage-Strassen to Harvey and van der
Hoeven's O(n log n) in 2019.
