# M/M/c

A pool of c servers sharing one queue. The Erlang C formula gives the
probability that an arriving case finds every server busy, and everything
else follows from it:

W_q = C(c, a) / (c·μ − λ), with a = λ/μ.

## The finding

Exercise 4.3 names eight employees and heads the section M/M/1. Both readings
are possible and they do not agree:

| Model | W_q | Target of one minute |
|---|---:|---|
| One counter at 80 calls/h | 1.25 min | missed |
| Eight clerks at 10 calls/h each | 0.33 min | met comfortably |
| Nine clerks at 10 calls/h each | 0.12 min | met |

Same total capacity, waiting times a factor of 3.7 apart. The single fast
server is the pessimistic model: a case that arrives during a long call waits
for that one call to end, while in the pool seven other calls are running and
one of them finishes soon.

Which answer the sheet wants depends on something the sheet does not say:
whether any clerk can take any call. If they can, it is a pool.
`what_the_sheet_asks` records both, because picking one silently would hide
the assumption that does the work.

## The check

At λ = 2, μ = 1, c = 3 the formula gives W_q = 0.444 and a simulation of two
hundred thousand customers gives 0.453. With c = 1 the formulas reduce to the
M/M/1 ones, which is the other check worth having.
