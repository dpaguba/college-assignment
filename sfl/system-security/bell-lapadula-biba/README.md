# Bell-LaPadula and Biba

Two rule sets with opposite goals. Bell-LaPadula protects secrecy: no read
up, no write down, so information never flows to a lower level. Biba protects
integrity: no read down, no write up, so a lower level never contributes to a
higher one.

Levels are counted as in the exercise, 0 the highest and 3 the lowest.

## The table of exercise 1.3b

| request | Bell-LaPadula | Biba | both |
|---|---|---|---|
| read 0 → 0 | yes | yes | yes |
| read 1 → 3 | yes | no | no |
| write 0 → 2 | no | yes | no |
| write 1 → 1 | yes | yes | yes |
| write 3 → 2 | yes | no | no |
| read 3 → 2 | no | yes | no |

That reproduces the published solution line for line.

## Why they cannot both be applied

The two rule sets are mirror images. Whatever one permits across levels, the
other forbids. `combined_report` counts every request over four levels and
finds **zero** permitted requests between different levels: only the diagonal
survives. Applying both means data can move within a level and nowhere else,
which is not a policy but a wall.

That is the answer to part (c), and it is measured rather than asserted.
