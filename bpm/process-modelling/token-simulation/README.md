# The token game

Tokens live on flows, not on nodes. The initial marking is one token on the
flow out of the start event; a token on the flow into an end event is a
finished case. Start and end events do not fire, which is the workflow-net
convention and makes the final marking something you can read off.

Every node contributes two choices: which incoming flows it consumes from
and which outgoing flows it produces on.

| Node | Consumes | Produces |
|---|---|---|
| task, intermediate event | its one incoming flow | its one outgoing flow |
| XOR | one marked incoming flow | one outgoing flow |
| AND | one token from every incoming flow | all outgoing flows |
| OR split | its incoming flow | any non-empty subset |
| OR join | every marked incoming flow | its outgoing flow |

## The inclusive join

It is the only rule that needs to look at the rest of the net. It may fire
when at least one of its incoming flows is marked and no token anywhere else
can still reach it. `_can_still_arrive` searches the graph forward from every
other token and asks whether the join is reachable without passing through
it. That is what makes the inclusive gateway expensive, and it is the reason
the soundness module leaves it out.

## What comes out

`traces` returns the sequences of tasks that reach the final marking, and
`markings` the reachable states. For two tasks between a parallel split and
join: two traces (a then b, b then a) and six markings. Between an inclusive
pair: four traces, because either branch alone is also a case. Between an
exclusive pair: two traces of one task each.

Loops make the number of traces infinite, so `traces` takes a limit on the
number of tasks in one trace.
