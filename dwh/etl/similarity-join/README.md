# Similarity join

Pairing records that do not match exactly. The naive version compares every
pair, which is quadratic: 40 000 comparisons for 200 records.

Blocking compares only records sharing a key, which brings the same case to
13 290 comparisons across ten blocks. The saving grows with the data, since
the number of blocks grows and the size of each does not.

## What blocking costs

A pair whose key differs is never compared, however similar it is. Two
spellings differing in the first letter are at edit distance one and land in
different blocks, and the module demonstrates exactly that case.

The usual repair is to block on something less fragile, such as a phonetic
code or several keys at once, which lowers the miss rate and raises the
number of comparisons. There is no setting at which the method is both exact
and subquadratic.
