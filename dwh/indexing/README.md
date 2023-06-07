# Indexing

| Topic | |
|---|---|
| [bitmap-indices](bitmap-indices/) | a bitmap per value |
| [wah-compression](wah-compression/) | runs, aligned to words |
| [bloom-filters](bloom-filters/) | false positives, never false negatives |
| [join-indices](join-indices/) | the join, stored |

Part V's second half. Every structure here trades space and maintenance for
query time, and the warehouse workload is what makes the trade pay: the data
is loaded once and read many times, so a cost per load is cheap and a cost
per query is not.

The exercise sheet's bitmap comes out at three WAH words for 124 bits, and
the conjunction is computed without decoding either side, which is the
property the alignment exists for.
