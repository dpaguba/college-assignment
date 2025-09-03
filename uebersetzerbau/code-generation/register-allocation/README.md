# Register allocation by graph colouring

Two variables may share a register exactly when they are never live at the same
time. Build a graph with an edge for every pair that is, and an allocation to
`k` registers is a colouring with `k` colours.

The graph does not care what the instructions do, only when values are needed,
which is why liveness analysis and register allocation are always adjacent in a
compiler.

## Optimistic colouring is not a detail

The classic algorithm removes nodes of degree less than `k`, since such a node
can always be coloured after its neighbours. When no such node exists, one is
spilled to memory.

On a four-variable cycle with two registers, **every** node has degree two, so
the pessimistic version spills immediately. The graph is plainly two-colourable,
opposite corners sharing a colour, and the measured result confirms it:

| graph | clique lower bound | registers this needs |
|---|---|---|
| 4-cycle | 2 | **2** |
| 4-clique | 4 | 4 |

Briggs' fix is one word: push the node anyway and mark it a **potential** spill,
then try to colour it on the way back and spill only if no colour is free.

## When a spill is unavoidable

Four variables all live at once form a clique, and no colouring with fewer than
four colours exists. With two registers the allocator keeps two and spills two,
which is not a weakness of the heuristic: the clique lower bound says four
colours are needed, so any allocator spills here.

Which node to spill when there is a choice is where real allocators differ. The
cost estimate is weighted by loop depth, because spilling inside a loop is far
more expensive than outside one.
