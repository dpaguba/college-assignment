# ETL

| Topic | |
|---|---|
| [extraction](extraction/) | what the source will tell you |
| [transformation](transformation/) | distances, codes, and formats |
| [similarity-join](similarity-join/) | matching without comparing all pairs |
| [loading](loading/) | the tricks, and the reason behind them |

Part VI, and the part of a warehouse project that takes most of the effort.
Three findings carry the block.

A timestamp column cannot see a delete, so the warehouse silently keeps rows
the source has removed. A date parser cannot tell 05.03 from 03/05 without
the separator, so the format has to be decided rather than detected. And
blocking a similarity join misses any pair whose key differs, which is a real
miss and not an approximation of one.
