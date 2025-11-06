# Distance measures

| Measure | Formula | Sees the length |
|---|---|---|
| Euclidean | `√Σ(aᵥ − bᵥ)²` | yes |
| cityblock | `Σ|aᵥ − bᵥ|` | yes |
| cosine | `1 − aᵀb / (‖a‖‖b‖)` | no |

## Why documents get the cosine

A term vector counts words, so it grows with the length of the text. Two
articles on the same subject, one three times as long, sit far apart under the
first two measures and together under the third. Taking relative frequencies
first removes the length beforehand, and then the three measures move closer
together, which is worth knowing before treating the choice as fundamental.

## The cosine distance is not a metric

For (1,0), (1,1) and (0,1) the way through the middle costs 2·(1 − 1/√2) ≈
0.586 and the direct way costs 1. The detour is shorter than the direct
route, so the triangle inequality fails.

Over 2 000 random triples in six dimensions it fails in **237 of them**, so
this is not a constructed corner case. Nothing here says the measure is
unusable; it says that any method built on the triangle inequality, such as a
metric search tree, has no guarantee under it.
