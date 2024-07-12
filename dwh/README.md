# Data Warehousing

Twenty modules in five blocks, following the seven parts of the lecture.

| Block | |
|---|---|
| [modelling](modelling/) | the four steps, star and snowflake, changing dimensions |
| [querying](querying/) | OLAP operations, star joins, materialized views |
| [indexing](indexing/) | bitmaps, WAH, Bloom filters, join indices |
| [etl](etl/) | extraction, cleaning, matching, loading |
| [mapreduce](mapreduce/) | the model, joins, aggregation, cost |

## The exercises, reproduced

The fifth sheet's bitmap, 1 zero followed by 20 ones, 3 zeros, 79 ones and 21
zeros, encodes to three WAH words at a word length of 32: a literal, a fill
of two groups and a literal. That is 96 bits against 124, the decoding
returns the original exactly, and the conjunction of two encoded bitmaps is
computed without decoding either, which is what the sheet asks to
demonstrate.

## Numbers worth keeping

| | |
|---|---:|
| fact table against all dimensions together | 1000 to 1 |
| snowflake saving on the example schema | 0.1 percent, for one extra join |
| star join: naive against bitmap plan | 1 000 000 against 1 000 fact rows |
| join order: selective first against last | 15 000 against 505 000 rows |
| aggregates of a cube with 10 dimensions | 1024 |
| Bloom filter, 1024 bits and 50 items | 0.001 false positives |
| blocking a similarity join on 200 records | 40 000 against 13 290 comparisons |
| MapReduce: optimal reducers with and without a combiner | 10 against 3 |

## Three results that argue with the first guess

**A timestamp column cannot see a delete.** Incremental extraction by
timestamp is the standard method and it silently keeps rows the source has
removed, because a deleted row has no timestamp left to read.

**Normalising a dimension saves nothing worth having.** On the example schema
it saves a tenth of a percent of the bytes and costs a join on every query
that touches the attribute, because the repetition it removes is in the small
tables.

**More reducers make a job slower past a point.** The total cost has a
minimum, at ten reducers on the module's example and at three once a combiner
is added, so parallelism is a parameter to tune rather than a direction to
push.

## Verification

The WAH encoding is checked by decoding it back on several patterns
including the exercise's, and the conjunction computed on the compressed form
is compared with the one computed on the decoded bits. The Bloom filter's
predicted error rate is compared with ten thousand measured lookups. The two
MapReduce join plans are compared against each other, and the cube operations
are checked by confirming that a roll up preserves the total.
