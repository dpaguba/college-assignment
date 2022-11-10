# Response time analysis

The exact test for fixed priorities. A task's response time is its own cost
plus the interference from every higher priority task, and the interference
depends on the response time, so the equation is solved by iterating upwards
from the sum of the costs.

The exam's two task sets differ only in the third task:

| set | C | T | R₃ | D₃ | |
|---|---|---|---:|---:|---|
| a | 1, 4, 10 | 5, 10, 25 | 28 | 25 | misses |
| b | 1, 4, 6 | 5, 10, 20 | 18 | 20 | fits |

Both fail the utilisation test, so the exact analysis is what separates them.
The iteration for set b goes 6, 12, 17, 18, 18, and the sequence increases
and is bounded, which is why it terminates.

## The analysis and the simulation agree

Every result here is checked against a simulator that runs the task set for a
hyperperiod and records misses. The analysis is a claim about the worst case
and the simulation is one particular execution, so they can disagree only if
one of them is wrong, and on both exam sets they do not.
