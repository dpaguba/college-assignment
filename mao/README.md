# Modellgestützte Analyse und Optimierung

Twenty-one modules in five blocks, following the twelve chapters of the
lecture: simulation in the first half, optimisation in the second.

| Block | |
|---|---|
| [simulation-concepts](simulation-concepts/) | the engine, the queue, validation |
| [random-numbers](random-numbers/) | generators, tests, transformations |
| [input-modelling](input-modelling/) | choosing and testing a distribution |
| [output-analysis](output-analysis/) | intervals, warm-up, batching |
| [optimisation](optimisation/) | convexity, LP, duality, integer, dynamic, heuristics |

## The published solutions, reproduced

The tenth sheet's production problem comes out exactly as printed: 300 units
of the first product and 150 of the second, a profit of 1500, with the
machine hours and the raw material both binding. The shadow prices follow at
0.5 and 0.3, with zero for the slack market constraint.

The ninth sheet's lists of advantages, disadvantages and typical mistakes are
reproduced as data, so the module can be used to check that nothing was
forgotten.

## Numbers worth keeping

| | |
|---|---:|
| M/M/1 at half load: simulation against formula | 1.974 against 2.0 |
| queue at 99 percent load | 99 customers |
| correlation of consecutive queue observations | 0.96 |
| the same after batching into 20 | -0.07 |
| interval ignoring that correlation | 8 times too narrow |
| antithetic variates, variance | 0.0889 to 0.0056 |
| knapsack: optimum against greedy | 220 against 160 |
| branch and bound against enumeration | 5 nodes against 961 |
| Fibonacci: plain against memoised | 21 891 calls against 39 |

## Three results that argue with the first guess

**An interval computed from simulation output is not slightly optimistic, it
is wrong by an order of magnitude.** Consecutive observations of a queue at
80 percent load correlate at 0.96, and the usual interval comes out eight
times too narrow. Batching fixes it and nothing else in the analysis does.

**A stream can pass a uniformity test and be entirely predictable.** The
alternating stream 0.25, 0.75, 0.25, … passes a chi-square test over two
buckets and has a serial correlation of minus one.

**An empirical distribution can never produce the value that matters.** It
puts equal weight on the observations and nothing beyond them, so the tail
that fills a queue's buffer is exactly what it cannot supply.

## Verification

The simulator is checked against the closed forms of the M/M/1 queue, the
generator against measured periods and the Hull and Dobell conditions, the
linear program against the published solution and against a full vertex
enumeration, branch and bound against enumeration of every integer point, and
the shadow prices against the direct experiment of relaxing each bound by one
unit.
