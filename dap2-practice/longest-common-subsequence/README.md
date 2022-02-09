# Longest common subsequence

LCS by dynamic programming. Practical sheet 7, tasks 7.1 and 7.2.

```
java LongestCommonSubsequence ABACABC BACCABBC
A: ABACABC
B: BACCABBC
LCS BACABC mit Laenge 6 gefunden.
```

## The recurrence

```
C[i][j] = C[i-1][j-1] + 1                      if a[i] = b[j]
C[i][j] = max(C[i-1][j], C[i][j-1])            otherwise
```

Θ(n·m) time and space. The border of zeros in row 0 and column 0 is what
removes every special case: the empty prefix has an LCS of length zero against
anything.

## Reconstruction without the second string

`LCS(int[][] C, String A)` gets the table and A, and that is enough. Walking
back from the bottom right corner: a cell that equals the one above it was not
produced by a match, so the row can be dropped; likewise for the column;
anything else came from the diagonal and that character belongs to the answer.
The table already records where the matches were, so B is never needed. O(n + m).

The LCS is not unique when there are ties, and the order of those two tests
decides which one comes out. The length is the same either way.

## Task 7.2: measurements

Three runs per size, median, milliseconds:

| n | LCSLaenge | LCS |
|---|---|---|
| 500 | 4.55 | 0.03 |
| 1000 | 2.22 | 0.06 |
| 2000 | 9.61 | 0.17 |
| 4000 | 39.83 | 0.74 |
| 8000 | 232.86 | 1.00 |

The table quadruples per doubling and the reconstruction roughly doubles, which
is Θ(n²) against Θ(n + m). The first row is warm-up noise.

The table is also where the memory goes: 8000 × 8000 ints is 256 MB. Only the
length is needed if the subsequence itself is not, and then two rows suffice, at
Θ(min(n, m)) space. Reconstruction is what forces the full table, and
Hirschberg's algorithm gets it back to linear space by splitting the problem in
half and recursing, at twice the time.

## Verification

Both examples from the sheet match exactly, including the reconstructed
subsequences `BACABC` and `EoCAXY`, which also confirms the random generator
and the tie-breaking order. All six error cases match.
