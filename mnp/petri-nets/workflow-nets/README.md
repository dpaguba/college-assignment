# Workflow nets and BPMN

A workflow net has one source place, one sink place, and every node on a path
between them. Soundness then packages three requirements into one criterion:
the final marking is reachable from every reachable marking, no marking has a
token in the sink alongside anything else, and no transition is dead.

| Fragment | Markings | Workflow net | Sound |
|---|---|---|---|
| sequence | 3 | yes | yes |
| AND-split with AND-join | 6 | yes | yes |
| XOR-split with XOR-join | 3 | yes | yes |
| AND-split with XOR-join | 5 | yes | **no** |

The last row is the error worth knowing. An AND-split starts two branches and
an XOR-join fires as soon as either arrives, so the case completes while the
other branch is still running, and its token is still in the net afterwards.
Proper completion fails. In BPMN this is drawn as a diamond with a plus
feeding a diamond with a cross, it looks entirely reasonable, and the net says
it is wrong.

## What BPMN borrows

A BPMN diagram has no semantics of its own. Each element stands for a net
fragment, and once the diagram is a net, the modeller's questions are the
standard net properties: can it deadlock, will it always finish, can it leave
work behind. Soundness is the name for wanting all three.

| Pattern | Places | Transitions |
|---|---|---|
| task | 2 | 1 |
| sequence | 3 | 2 |
| parallel gateway | 4 | 2 |
| exclusive gateway | 3 | 2 |

The two gateways use the same number of transitions and a different number of
places, and the place count is where the difference lives. A parallel gateway
puts a token in each branch; an exclusive gateway has one place that two
transitions compete for. Concurrency and choice are structurally different in
the net even where the diagram distinguishes them by a symbol inside a
diamond.
