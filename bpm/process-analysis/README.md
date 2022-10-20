# Process analysis

The quantitative half of the course. Flow analysis estimates performance
from what is known about the activities; queueing adds the waiting that
comes from resources being busy; simulation drops the assumptions and plays
cases through.

| Module | Topic |
|---|---|
| [flow-analysis](flow-analysis/) | cycle time of a block-structured model |
| [cycle-time-efficiency](cycle-time-efficiency/) | how much of the time is work |
| [rework-loops](rework-loops/) | what a repeated check costs |
| [littles-law](littles-law/) | WIP = λ · CT |
| [capacity-and-utilisation](capacity-and-utilisation/) | μ = uc/ul and ρ = λ/μ |
| [queueing-mm1](queueing-mm1/) | one server, exponential times |
| [queueing-mmc](queueing-mmc/) | a pool of servers, Erlang C |
| [process-simulation](process-simulation/) | duration, cost and spread from many cases |

Every result in this block was checked a second way. The flow analysis
against exhaustive enumeration over all branch combinations, which is exact
rather than sampled and agrees to the last digit. The queueing formulas
against a simulated queue with exponential inter-arrival and service times.
Little's law against the measured average number in a simulated system.
