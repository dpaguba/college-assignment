# Output analysis

| Topic | |
|---|---|
| [confidence-intervals](confidence-intervals/) | the interval and its assumption |
| [transient-phase](transient-phase/) | throwing away the start |
| [batch-means](batch-means/) | one run, several observations |
| [run-length](run-length/) | how long, and why it is quadratic |

Chapter five, and the block that separates a simulation result from a number.

The measurement that carries it: on a queue at 80 percent load, consecutive
observations have a correlation of 0.96, and an interval computed as though
they were independent comes out eight times too narrow. Batching brings the
correlation to -0.07 and the interval to something that means what it says.
