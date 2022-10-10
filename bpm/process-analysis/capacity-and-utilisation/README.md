# Capacity and utilisation

Theoretical capacity μ = uc/ul: the number of resource units divided by the
time one unit needs per case. Eight clerks at half an hour each handle
sixteen cases an hour.

Utilisation ρ = λ/μ. Above one the pool is overloaded and the queue grows
without bound; there is no steady state to compute and nothing to optimise.

## Why full utilisation is not the goal

It looks efficient and it is the thing managers count. A pool at 100 % has no
reserve: every absence and every unusually long case turns directly into
waiting time. The queueing formulas make this precise, since waiting grows
like 1/(1 − ρ) and runs away well before ρ reaches one.

`assess` says so at three levels: over one is not sustainable, over 0.9 means
every fluctuation shows up as waiting, below that the pool copes. For people
rather than machines the practical ceiling is around 0.8.

`bottleneck` returns the busiest pool, which is where any improvement has to
start: making a non-bottleneck faster changes the total by nothing.
