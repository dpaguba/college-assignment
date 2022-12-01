# Connectors

| Connector | Branches taken | The join waits for |
|---|---|---|
| XOR | exactly one | the one branch that ran |
| OR | at least one | the branches that ran |
| AND | all | all branches |

## The rule that is specific to this notation

After an event there may be no deciding split. XOR and OR choose, and an
event cannot choose: it is passive, it states that something has happened.
Only a function can decide, because deciding is doing something.

`may_follow` tests exactly that, and it distinguishes the three cases that
are allowed anyway: a join after an event is fine, an AND split after an
event is fine (it does not choose, it goes both ways), and any split after a
function is fine.

## The inclusive join

It has to know which branches actually ran, and that information sits at the
split far upstream, not at the join. Executable notations therefore restrict
it or forbid it. The EPK allows it, and it can, because an EPK is not
executed: it is read by people who can work out what was meant.
