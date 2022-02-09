# Maximum subproduct

The largest product of a contiguous range. Practical sheet 6, task 6.2.

```
java MaxProdDemo
unsigned: [4,5,8]
signed:   [0,2,24]
4000 zufaellige Instanzen gegen Brute Force geprueft.
```

`Range` and `MaxProd` are the submission; the demo class only checks them.

## The recurrence

d[r] is the best product of a range ending at r:

```
d[0] = a[0]
d[r] = max(a[r], d[r-1] · a[r])
```

Either the range starts here or it extends the best one ending at the previous
position. Then p_max is the largest d[r]. Θ(n), the multiplicative twin of
Kadane's algorithm for the maximum subarray sum.

## What negatives break

Everything. With a negative factor the *worst* product ending at r−1 becomes
the best one ending at r. So `buildTableSigned` carries a second table, the
smallest product ending at each position, and the two swap roles across a sign
change. Each is the max or min of the same three candidates: start fresh,
extend the best, extend the worst.

Keeping more state than the question asks for is the standard fix when a
recurrence fails: the quantity you want is not self-sufficient, so you carry
what it depends on.

## Recovering the indices

`compute` finds the largest table entry for the right end, then multiplies
leftwards until the running product equals it. That must terminate, because the
entry was built from exactly that suffix. Nothing in it assumes positivity, so
one method serves both tables, which is what the sheet predicts in part (c).

## BigDecimal, not double

A product of a few hundred decimals loses precision fast, and the comparisons
that drive the algorithm would then be decided by rounding error. Comparisons go
through `compareTo` and never `equals`, because `BigDecimal.equals` also
compares the scale: 2.0 and 2.00 are unequal to it.

## Verification

4000 random instances against brute force over every range, half with negative
values. The unsigned table was checked on the non-negative half only, since that
is all it claims.
