# The winner's curse

Every configuration is in truth equally good. They are measured on the same
validation set, so the measurements differ only by chance. Taking the best one
takes the largest upward fluctuation with it.

| configurations tried | bias |
|---:|---:|
| 1 | 0.0004 |
| 2 | 0.007 |
| 5 | 0.016 |
| 20 | 0.026 |
| 100 | 0.034 |
| 500 | **0.041** |

It grows like a logarithm: ten times as many candidates do not cost ten times
the bias, but it grows without bound. Search long enough and something will
always look good.

## The size of it is predictable

The expected maximum of k standard normals, against the approximation
`Φ⁻¹((k − 0.375)/(k + 0.25))`:

| k | measured | approximation |
|---:|---:|---:|
| 2 | 0.577 | 0.589 |
| 10 | 1.539 | 1.547 |
| 100 | 2.507 | 2.499 |
| 1000 | 3.238 | 3.227 |

So the bias is not merely observed but predicted: it is this number times the
standard error of a single measurement. A larger validation set therefore
shrinks it, and more candidates grow it.

## What removes it

A third set that played no part in the selection. That costs data and nothing
else, and it is the only reliable route.

## Why this is the same problem the offline RL topic describes

A method whose settings were chosen on the data it is reported on looks better
than one whose settings were fixed, even when the two are equally good, and
the lead grows with how much compute someone had. One of the thesis offers
names exactly this as a fundamental flaw in offline reinforcement learning
evaluation. The finding is not specific to that field.
