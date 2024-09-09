# Replacement policies

When a set is full, something must go, and which one is a prediction about the
future made from the past.

## Belady's anomaly, measured

LRU is a **stack algorithm**: the contents of a cache with `n` ways are always
a subset of one with `n+1` ways, so more capacity can never cause more misses.
FIFO is not, and on the classic reference string:

| policy | 3 ways | 4 ways |
|---|---|---|
| FIFO | 0.750 | **0.833** |
| LRU | 0.833 | 0.667 |

The larger FIFO cache misses **more often**. That is not a rounding artefact,
it is the anomaly, and it is the reason "bigger is at least as good" needs a
proof rather than an intuition.

## The optimal policy is the bound

Belady's optimal policy evicts whatever is needed furthest in the future. It is
unimplementable, and useful precisely for that: it is the lower bound every
real policy is measured against, and a policy close to it has little left to
gain from being cleverer. Verified here to be at least as good as both LRU and
FIFO on the same stream.
