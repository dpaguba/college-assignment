# Periodic tasks on one processor

Two tests, and the difference between them is the point.

| tasks | 1 | 2 | 3 | 4 | 10 | 100 |
|---|---:|---:|---:|---:|---:|---:|
| rate monotonic bound | 1.000 | 0.828 | 0.780 | 0.757 | 0.718 | 0.696 |

The bound falls towards the natural logarithm of two, which is where the
familiar 69 percent comes from. It is **sufficient and not necessary**: a set
above it may still be schedulable, and the exam's second task set is exactly
such a case, with a utilisation of 0.9 against a bound of 0.78 and a
perfectly feasible schedule.

The earliest deadline first test is sufficient and necessary. For implicit
deadlines a set is schedulable exactly when its utilisation fits, so nothing
else about the periods matters.

That is the trade the two policies make. Fixed priorities are cheaper to
implement and lose up to 30 percent of the processor; dynamic priorities use
all of it and cost a comparison at every scheduling point.
