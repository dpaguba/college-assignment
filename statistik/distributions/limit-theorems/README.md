# Limit theorems

Two statements that are often merged and are not the same.

**The law of large numbers** says the sample mean approaches the expectation.
Measured on the modified die: the average of 20 000 draws is within 0.05 of
3.5, and the average absolute error falls by roughly half when the sample
size is quadrupled, which is the square root rule.

**The central limit theorem** says more: the standardised sum approaches a
normal distribution whatever the original was. Measured as the largest gap
between the empirical distribution of the standardised sums and the normal
one:

| summands | 1 | 2 | 5 | 10 | 40 |
|---|---:|---:|---:|---:|---:|
| distance | 0.203 | 0.135 | 0.064 | 0.052 | 0.034 |

The first says where the average goes, the second says how it is spread on
the way, and only the second explains why the normal distribution appears in
places where nothing is obviously normal.

## Chebyshev's inequality

The third statement, and the weakest: at least 1 - 1/k² of any distribution
lies within k standard deviations, whatever the shape.

| k | Chebyshev | normal |
|---|---:|---:|
| 1.5 | 0.444 | 0.134 |
| 2 | 0.250 | 0.046 |
| 3 | 0.111 | 0.003 |

The bound is loose by a factor of three to forty against a normal
distribution, and it is the price of assuming nothing. It is what makes the
law of large numbers provable without knowing the distribution at all.
