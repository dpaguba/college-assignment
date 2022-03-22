# Memory organisation

A memory of `n` words needs `log2 n` address bits and a decoder turning them
into one word line. A flat decoder for a million words needs a million output
lines, which is why memories are two-dimensional: a row decoder and a column
decoder, about `2 * sqrt(n)` lines instead of `n`.

## SRAM against DRAM

| | transistors per cell | refresh | use |
|---|---|---|---|
| SRAM | **6** | no | caches, registers |
| DRAM | **1** plus a capacitor | every few milliseconds | main memory |

Six times the area against a refresh controller and a slower access. That
single ratio decides the whole memory hierarchy: everything close to the
processor is SRAM because it must be fast, and everything large is DRAM because
it must be cheap.

## Row hits are not an implementation detail

Reading a DRAM row destroys it and it must be written back, so an access that
hits an already-open row is much cheaper than one that does not. That asymmetry
is why memory controllers reorder requests and why a sequential access pattern
is worth so much more than a random one.
