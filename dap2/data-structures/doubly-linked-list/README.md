# Doubly linked list

Every node knows both neighbours, so removing one is three assignments.

| Operation | Cost |
|---|---|
| Push or pop at either end | O(1) |
| Remove a node you hold | O(1) |
| Find a value | O(n) |
| Index | O(n) |

| | |
|---|---|
| Memory | O(n), two pointers per element |
| Ordered | by position, not by key |

## The idea

An array stores elements next to each other, so removing from the middle shifts
everything after it. A list stores a pointer instead, so removal is local: unlink
the node and nothing else moves.

The backward pointer is the whole reason a doubly linked list exists. With only a
forward pointer, removing a node requires finding its predecessor first, which is a
scan. With both, removal is O(1) given the node.

## How it works

Two sentinel nodes sit at the ends, so no operation ever has to ask whether it is
at a boundary. Insertion links a new node between two existing ones; removal points
the neighbours at each other.

`find` is the O(n) part and `remove` is the O(1) part, which is why the useful
pattern is to keep the node around rather than the value.

## The trade

An array reaches element 1000 by arithmetic; a list walks a thousand pointers, each likely a cache miss. That is why arrays win in practice far more often than the complexity table suggests.

## Where it is used

Anywhere something must be unlinked from a position it already occupies: LRU caches moving an entry to the front, scheduler run queues, editor undo histories, and the intrusive lists throughout the Linux kernel.
