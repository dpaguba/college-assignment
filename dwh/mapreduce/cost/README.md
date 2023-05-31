# What a job costs

Map time, network, reduce time, and a fixed overhead per reducer. More
reducers shorten the reduce phase and add overhead, so the total has a
minimum:

| | optimal reducers | total |
|---|---:|---:|
| without a combiner | 10 | 1600 |
| with a combiner keeping a tenth | 3 | 1082 |

Two things follow. Adding reducers past the optimum makes the job slower, so
"more parallelism" is not a strategy. And a combiner does not only lower the
total, it lowers the optimal number of reducers, because it removes the term
that more reducers were being added to divide.

The cheapest change available is therefore the combiner: no extra machines,
no change to the algorithm beyond a combinable measure.
