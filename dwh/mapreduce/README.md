# MapReduce

| Topic | |
|---|---|
| [mapreduce-model](mapreduce-model/) | map, shuffle, reduce |
| [joins](joins/) | broadcasting the small side |
| [aggregation](aggregation/) | which measures combine |
| [cost](cost/) | where the minimum is |

Part VII. The model is small and the two questions that decide performance
are both about the key: how evenly it spreads the work, and whether the
measure keyed by it can be combined.

The measured results: a skewed key sends 100 percent of the work to one
reducer, and a combiner lowers the optimal number of reducers from ten to
three while lowering the total by a third.
