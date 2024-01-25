# Business Process Management

The course follows Dumas et al., *Fundamentals of Business Process
Management* (2021). Twenty-seven modules in four blocks, one per topic of
the lecture: how an organisation finds its processes, how it models them,
how it measures them, and what a machine can do with the result.

| Block | Modules | What it holds |
|---|---:|---|
| [process-architecture](process-architecture/) | 5 | the lifecycle, categories, relations, the map, the portfolio |
| [process-modelling](process-modelling/) | 10 | BPMN elements, gateways, the token game, soundness, data |
| [process-analysis](process-analysis/) | 8 | flow analysis, Little's law, queues, simulation |
| [process-technology](process-technology/) | 4 | what a BPMS is, what it cannot read, redesign |

## What makes the subject implementable

A process model is a graph. Once it is a data structure the rest of the
course computes: the token game gives the set of traces, the traces show
deadlock and lost synchronisation, flow analysis is the same recursion over
the same blocks with times instead of tokens, and simulation is that
recursion again with random draws. The numbers on the exercise sheets become
test cases.

None of the sheets came with solutions, so every number here was derived and
then checked a second way: the flow analysis against exhaustive enumeration
over all branch combinations, the queueing formulas against a simulated
queue, the reachability graph in `soundness` against the independent one in
`token-simulation`.

## The numbers that came out

| Exercise | Result |
|---|---|
| Loan application, no rework | 8.4 days |
| The same with a 20 % incomplete-form rate | 8.65 days |
| Its cycle time efficiency | 8.9 work hours in 69.2 hours, 12.9 % |
| App release, inclusive gateway | 24.6 hours |
| Exposé process | 68 hours, 28.5 of them work, 41.9 % |
| Application form | 41.2 minutes |
| Restaurant, peak and off peak | 36 minutes both times |
| Call centre as one counter at 80 calls/h | 1.25 min waiting, target missed |
| The same at 90 calls/h | 0.83 min, target met |
| The same as eight clerks at 10 calls/h each | 0.33 min, target met comfortably |

The last three lines are the finding worth keeping: the answer to exercise
4.3 depends on whether the eight clerks are modelled as one fast counter or
as eight slow ones. Same total capacity, waiting time 3.7 times apart.
