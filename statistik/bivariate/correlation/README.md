# Correlation

The children's data of the third sheet: ages `9, 6, 12, 10, 8, 9` and heights
`130, 125, 145, 140, 130, 140`.

| | |
|---|---|
| covariance | 14 |
| standard deviations | 2 and 7.746 |
| correlation | 0.904 |

All reproduced from the published solution, and the correlation agrees with
numpy to nine decimals.

The covariance carries the units of both variables, so multiplying heights by
three multiplies it by three, and nothing can be read from its size alone.
Dividing by the two standard deviations removes the units and bounds the
result by one, which is the whole reason for the correlation coefficient.

## What it measures, and what it does not

Pearson's coefficient measures linear association. The points of a symmetric
parabola have correlation exactly zero and complete dependence, since one
variable determines the other, and the module includes that example.

Spearman's version applies the same formula to the ranks, so it survives any
monotone transformation: squaring the heights leaves it unchanged. On data
lying on a rising curve it gives 1 where Pearson gives less, because it asks
whether the two rise together rather than whether they do so in a straight
line.
