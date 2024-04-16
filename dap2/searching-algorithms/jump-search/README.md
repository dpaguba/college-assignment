# Jump search

Skip forward in blocks of √n, then walk through one block.

| | |
|---|---|
| Average | O(√n) |
| Worst | O(√n) |
| Memory | O(1) |
| Needs | a sorted array |
| Answers | where is this value |

## The idea

Step forward in blocks until a block's last element is not smaller than the target,
then scan that block linearly.

With block size b the cost is n/b jumps plus b steps. Minimising n/b + b gives
b = √n, so the whole search is 2√n comparisons. Slower than binary search, and
chosen anyway when moving backwards is expensive: on tape, or a singly linked list,
binary search's bouncing between distant positions costs far more than the extra
comparisons here, because jump search only ever moves forward.

## How it runs

1. Jump in steps of √n while the element at the block boundary is smaller.
2. Scan the final block from its start.

## When it is the right choice

Sequential media, and structures where a backward seek costs more than a forward one.
