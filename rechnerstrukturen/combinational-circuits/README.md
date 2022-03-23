# Combinational circuits

| Topic | |
|---|---|
| [logic-circuits](logic-circuits/) | gates, size against depth, the standard blocks |
| [adders](adders/) | the carry chain and the two ways around it |
| [multipliers](multipliers/) | shift and add, arrays, Booth |
| [hazards](hazards/) | correct logic with a wrong output |

The first three are about making a function fast, and the fourth is about the
fact that "fast" and "correct at every instant" are different properties. A
combinational circuit is only guaranteed correct once its inputs have been
stable long enough, which is what the clock in the next block is for.
