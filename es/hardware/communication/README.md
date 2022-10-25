# Communication

| | who sends | worst case wait |
|---|---|---|
| CAN | the smallest identifier | none |
| TDMA | the node whose slot it is | one round |

A priority bus never delays an important message behind an unimportant one,
and it gives a low priority message no bound at all: a busy bus can starve it
indefinitely. A slotted bus bounds everything and wastes the bandwidth of a
silent node.

That is the same trade as between dynamic and static priorities in the
scheduling block, one level down, and it is decided the same way: by whether
a bound is needed or an average.

A frame in flight cannot be interrupted, so even the highest priority message
waits for the longest frame currently being sent. That blocking is bounded
and it has to enter the analysis, exactly like resource blocking in a task
set.
