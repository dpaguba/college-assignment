# The event-based gateway

The data-based gateway evaluates a condition and chooses. The event-based
gateway does not choose at all: it waits, and the branch on which something
happens first wins.

That is why every branch of an event-based gateway has to begin with an
event. A task after it would start immediately and take the decision away
from the environment, which is the one thing the gateway exists to avoid.
`check_branches` refuses anything else.

The example from the lecture is a race between a message and a ten-minute
timer. `race` returns the winner and the discarded branch. A tie is reported
as undecided rather than resolved: the specification leaves it to the engine,
and pretending otherwise would put a made-up rule into the model.

| Gateway | Decides | Branch labels |
|---|---|---|
| data based | the process itself | conditions |
| event based | the environment | events |
