# The event-driven process chain

The notation of tutorials one and two. Five modules: the building blocks, the
connectors, the rules a model has to satisfy, and the two exercises.

| Module | Topic |
|---|---|
| [epk-elements](epk-elements/) | events, functions, connectors, control flow |
| [epk-connectors](epk-connectors/) | XOR, OR, AND and who may decide |
| [epk-wellformedness](epk-wellformedness/) | checking a chain against the rules |
| [order-intake](order-intake/) | the mail-order intake and its decision table |
| [goods-receipt](goods-receipt/) | goods receipt with two parallel checks |

Everything in the notation follows from one distinction: a function does
something, an event states that something is the case. Functions and events
therefore alternate, and an event cannot be followed by a decision, because
stating a fact is not choosing.
