# Eingebettete Systeme

Twenty-four modules in six blocks, following the six chapters of the lecture
and the ten questions of the 2020 exam.

| Block | |
|---|---|
| [models-of-computation](models-of-computation/) | dataflow, Kahn networks, state charts, discrete events |
| [hardware](hardware/) | sampling, efficiency, buses, power |
| [rtos](rtos/) | tasks, resources, priority inversion |
| [evaluation](evaluation/) | Pareto fronts, WCET, real-time calculus |
| [scheduling](scheduling/) | aperiodic, periodic, servers, multiprocessor |
| [optimisation](optimisation/) | ILP, exploration, energy |

## The exam, reproduced

| Question | Result |
|---|---|
| 9(a) RM feasibility | U = 1.0 against a bound of 0.78; response time 28 against a deadline of 25, infeasible |
| 9(b) RM feasibility | U = 0.9 against the same bound; response time 18 against 20, feasible |
| 9(c) aperiodic | earliest due date gives τ2, τ3, τ1 completing at 2, 11, 19 |
| 10 power aware design | optimal frequency 100 MHz, 0.18 mJ per period, 2000 hours of battery |
| 8(b) arrival curves | upper jumps to 2 at once, lower stays at 0 for a whole period |
| 5(c) sampling | 1000 Hz sampled at 1000 Hz cannot be reconstructed |
| 4(b) converters | flash 15 comparators and one step, successive approximation 1 and four |
| 3 state chart | the cookie machine, with history on the crunchiness |
| 7 Pareto | the dominated and dominating regions |

## Three results that argue with the rule

**Filling the slack is the worst DVFS strategy on this processor.** Stretching
the task to its deadline runs at 30 MHz and costs 0.405 mJ; the optimum runs
at 100 MHz and costs 0.18; running flat out costs 0.3. The textbook rule is
about switching energy and the exam is about a battery, and the static draw
reverses the answer.

**The optimal scheduling policy behaves worse under overload.** On a set with
utilisation 1.63, the simulator records 18 missed deadlines under rate
monotonic and 26 under earliest deadline first, because a job that will
already miss becomes the most urgent one.

**The utilisation test is sufficient and not necessary, and the difference is
the exam question.** Both of its task sets fail the bound; the exact response
time analysis passes one and fails the other.

## Verification

Every schedulability result is checked against a simulator that runs the task
set for a hyperperiod and records misses. The energy optimum is computed from
the closed form and confirmed by a search over the frequency range. Jackson's
rule is checked against every permutation of the jobs rather than cited. The
repetition vector of an SDF graph is confirmed by executing the schedule and
comparing the token counts with the initial ones.
