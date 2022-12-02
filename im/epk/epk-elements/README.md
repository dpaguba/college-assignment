# Elements

Four building blocks. The **event** is a hexagon and passive: it says that a
state has been reached. The **function** is a rounded rectangle and active: it
consumes time and resources. The **connector** branches or joins. The
**control flow** is the arrow between them.

## Why events and functions alternate

An event is a state, a function a transition. Two states in a row would leave
out the transition between them; two functions in a row the state between.
Either way half the story is missing, which is why the notation requires them
to alternate along the control flow. Connectors sit between them and do not
break the alternation.

## The extended chain

The plain chain shows only the sequence. The extended one attaches to each
function who performs it, which data it touches and which system supports it.
That is the step from a picture of a process to a basis for introducing a
system, and it is the only reason the notation survives in practice.
