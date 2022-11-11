# Evaluation and validation

| Topic | |
|---|---|
| [pareto-fronts](pareto-fronts/) | comparing designs without weights |
| [wcet-analysis](wcet-analysis/) | the longest path, and why measuring is not enough |
| [real-time-calculus](real-time-calculus/) | curves instead of traces |

Chapter five, and the block that supplies the numbers the scheduling block
consumes. A schedulability test needs a worst case execution time, and where
that number comes from is a subject of its own: measured values are lower
bounds and analysed values are upper bounds, and the gap between them is the
price of a guarantee.

Real-time calculus generalises the same move from one number to a curve. The
quantifier is what does the work: over **any** interval of a given length,
rather than over the intervals that happened to be observed.
