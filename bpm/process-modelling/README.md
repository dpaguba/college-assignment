# Process modelling

BPMN 2.0 as a data structure. Ten modules: the notation itself, then the
semantics, then the two things that only show up when the model is executed.

| Module | Topic |
|---|---|
| [bpmn-elements](bpmn-elements/) | the element catalogue and the pool rule |
| [sequence-flow](sequence-flow/) | the control flow as a graph |
| [gateways](gateways/) | XOR, AND, OR and matching splits to joins |
| [token-simulation](token-simulation/) | the token game, traces and markings |
| [soundness](soundness/) | the three conditions of an executable model |
| [event-based-gateway](event-based-gateway/) | deciding by data or by what happens first |
| [boundary-events](boundary-events/) | interrupting and non-interrupting exceptions |
| [subprocesses](subprocesses/) | collapsed for reading, expanded for running |
| [task-types](task-types/) | the seven types and which of them automate |
| [data-objects](data-objects/) | objects, stores, and reads with no writer |

The centre of the block is the token game. Everything the lecture says about
gateways is a rule for moving tokens, and once those rules are code, the
model answers questions instead of being argued about: which orders of work
are possible, whether the process can finish, whether some activity never
happens.
