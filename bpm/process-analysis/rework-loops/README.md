# Rework loops

A body that runs once and then repeats with probability r runs 1/(1 − r)
times on average. If it is entered only when needed, the first pass falls
away and r/(1 − r) is left.

| Rework rate | Passes |
|---|---:|
| 0 % | 1.00 |
| 10 % | 1.11 |
| 20 % | 1.25 |
| 50 % | 2.00 |
| 90 % | 10.00 |

The relation is not linear, and that is the whole content of the module. Ten
to twenty percent costs almost nothing. Fifty to ninety percent multiplies
the body by five. A check that fails nine times out of ten is not a check,
it is the process.

`simulate` counts the passes over two hundred thousand runs and lands on
1.25 for r = 0.2, which is the geometric mean it should be.

Rework comes from incomplete input, a failed check, or a rejected approval.
The cheapest place to remove it is before the case starts: validating the
form costs one pass, rejecting it later costs the whole body again.
