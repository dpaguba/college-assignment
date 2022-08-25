# Observables

A stream of values over time. Nothing happens until someone subscribes: the
module counts 0 values produced before the subscription and 3 after.

`map` and `filter` compose without touching the producer. Unsubscribing stops
the producer, not only the delivery: of 5 available values the producer emits
2 and then finds nobody listening, so the remaining three are never computed.
That is the difference from a collection, where all the work happens first.

An error ends the stream. Two values arrive, the error arrives, and the
completion never does, which the module records.

## Against a promise

A promise delivers one value, starts immediately, and cannot be cancelled. A
stream delivers many, starts on subscription, and can be. A single HTTP
request fits a promise; a series of user events does not.
