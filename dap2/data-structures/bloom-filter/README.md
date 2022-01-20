# Bloom filter

Says definitely not, or probably, and never stores the data.

| Operation | Cost |
|---|---|
| Add | O(k), k hash functions |
| Membership test | O(k) |
| Delete | impossible |
| Iterate | impossible |

| | |
|---|---|
| Memory | about 1.2 MB per million items at 1 percent error |
| Ordered | no |

## The idea

Every other structure here can tell you exactly what it holds, because it holds it.
A Bloom filter holds nothing. k hash functions map an item to k bit positions, and
adding it sets those bits; asking about an item checks the same bits.

That gives an asymmetry which is the entire point. If any bit is clear, the item was
definitely never added, so a negative answer is certain. If all are set, the item is
probably present, but the bits may have been set by others, so a positive answer can
be wrong.

**False positives happen. False negatives cannot.** Every use of the structure is
built on that one guarantee.

## How it works

Two parameters follow from minimising error for a given size: the bit count is
-n·ln(p) / ln(2)², and the number of hash functions is (m/n)·ln(2). Both are in the
constructor.

k independent hash functions are not needed in practice: two are enough, and the
rest are generated as `h1 + i·h2`, which is what this implementation does.

Deletion is impossible, because clearing a bit could erase an item that shares it.
Counting Bloom filters replace bits with small counters to allow it, at four times
the memory.

## The trade

Orders of magnitude less memory than a real set, in exchange for a tunable rate of wrong answers in one direction and no ability to enumerate, delete or retrieve.

## Where it is used

Anywhere something expensive sits behind a cheap check: databases skipping disk reads for keys the filter denies, browsers screening URLs against malware lists, CDNs avoiding a network call for objects known to be absent, and Bitcoin's SPV clients.
