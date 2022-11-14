# Models of computation

| Topic | |
|---|---|
| [dataflow-sdf](dataflow-sdf/) | fixed rates, and everything decided in advance |
| [kahn-networks](kahn-networks/) | determinism from a single prohibition |
| [state-charts](state-charts/) | hierarchy, parallel states, history |
| [discrete-event](discrete-event/) | time as data, and the loop that stops it |
| [thread-limits](thread-limits/) | what the default model cannot say |

Chapter two. Each model is a set of restrictions and a set of guarantees, and
the block is best read as a table of what each one buys.

Threads guarantee nothing and permit everything. Kahn networks forbid testing
a channel for emptiness and gain determinism. Synchronous dataflow fixes the
rates and gains a compile time schedule, buffer sizes and a deadlock check.
State charts add no computational power at all and remove the state explosion
that makes flat automata unreadable.

The exam's cookie machine is the concrete case: twelve flat states, or three
small machines with one history marker.
