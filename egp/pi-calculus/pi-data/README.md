# Data as processes

Exercise 9: encode the list [A, B, C] as a process reachable at a channel k.

A cell sends its value over the channel and then the channel at which the
rest of the list can be found. The rest sits behind a restriction so its
channel is fresh. The empty list sends the name `nil` and stops.

`read_back` encodes a list, runs a reader against it and records what
arrives: A, B, C in order, which is the proof that the encoding describes the
list rather than merely resembling one.

## Two things the exercise teaches by accident

**A cell sends twice** because the calculus transmits one name per reaction,
and a cell has to hand over both a value and the rest channel. The order is a
convention and not a type: swap it and the reader takes values for channels.
The polyadic π-calculus allows tuples and is exactly this decomposition,
abbreviated.

**Output blocks.** The first reader put its report as a prefix, `k(v).ḡot⟨v⟩.
k(rest)...`, and read exactly one element before stopping: in the synchronous
calculus an output waits until somebody receives it, and nothing receives on
`got`. Putting the report in a parallel branch fixes it. That is a property of
the calculus, not of the encoding, and it is easy to miss because the first
element does come through.
