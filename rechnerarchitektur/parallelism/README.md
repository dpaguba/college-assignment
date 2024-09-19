# Parallelism

| Topic | |
|---|---|
| [parallel-loops](parallel-loops/) | handing out iterations, and the two ways it goes wrong |
| [cache-coherence](cache-coherence/) | keeping private caches consistent |
| [interconnection-networks](interconnection-networks/) | the shapes and what each costs |

The three are the layers of a shared-memory machine seen from the top down: the
program that wants to be parallel, the hardware that has to make its memory
look shared, and the wires that carry the traffic this generates.

False sharing sits across all three: a program with no race and no shared data
generates coherence traffic, because the hardware works in cache lines and the
network has to carry it.
