# Scheduling

| Topic | |
|---|---|
| [aperiodic](aperiodic/) | Jackson's rule and its limits |
| [periodic-uniprocessor](periodic-uniprocessor/) | the utilisation tests |
| [response-time](response-time/) | the exact test for fixed priorities |
| [servers](servers/) | budgets for aperiodic work |
| [edf-vs-rm](edf-vs-rm/) | static against dynamic priorities |
| [multiprocessor](multiprocessor/) | why none of it carries over |

Chapter six, and the block the exam draws three questions from. All three are
reproduced: the first task set has response time 28 against a deadline of 25
and is infeasible, the second has 18 against 20 and is feasible, and the
aperiodic set completes at 2, 11 and 19 under earliest due date.

Every analytical result is checked against a simulator, because a test that
says a set is schedulable and a simulation that misses a deadline cannot both
be right. The simulator assumes nothing and is far slower, which is exactly
what makes it a usable oracle.
