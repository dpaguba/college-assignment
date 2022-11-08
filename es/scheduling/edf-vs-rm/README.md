# Static against dynamic priorities

Rate monotonic assigns priorities once, from the periods. Earliest deadline
first assigns them at every instant, from the absolute deadlines.

| | rate monotonic | earliest deadline first |
|---|---|---|
| priorities | static | dynamic |
| utilisation bound | 0.69 for many tasks | 1 |
| implementation | a fixed order | a comparison per event |
| behaviour under overload | sheds the lowest priority | misses cascade |

The last row is the one usually left out. On a set with utilisation 1.63 over
77 time units, the simulator records 18 misses under rate monotonic and 26
under earliest deadline first, because a job that will already miss its
deadline becomes the most urgent one and takes the processor from jobs that
could still have finished.

So the optimal policy is optimal exactly while the assumptions hold, and it
degrades worse than the suboptimal one when they do not. Which behaviour is
wanted is a design decision, not a theorem.
