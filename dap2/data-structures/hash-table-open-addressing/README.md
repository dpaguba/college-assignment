# Hash table with open addressing

No lists: on a collision, probe forward for the next free slot.

| Operation | Cost |
|---|---|
| Insert | O(1) average, O(n) worst |
| Search | O(1) average, O(n) worst |
| Delete | O(1) average, leaves a tombstone |
| Ordered traversal | not possible |

| | |
|---|---|
| Memory | O(capacity), and capacity is at least twice the count |
| Ordered | no |

## The idea

Chaining hangs a list off each bucket. Open addressing has no lists at all:
everything lives in one flat array, and a collision probes forward for the next free
slot.

One contiguous array means a lookup touches one cache line instead of chasing
pointers, and that is why real implementations, Python's own dict included, are
built this way.

Deletion is the awkward part. Emptying a slot would break every probe sequence that
passed through it, so a deleted slot gets a tombstone: probing continues past it,
but an insert may reuse it. Tombstones accumulate, which is another reason to
rehash.

## How it works

Probe quadratically, at offsets 1, 4, 9, 16, rather than linearly. Linear probing
makes occupied slots clump into runs, and every run makes the next collision more
likely, a feedback loop called primary clustering.

Grow at half full rather than three quarters: open addressing degrades far more
sharply as it fills, because probe sequences lengthen for everybody at once.

## The trade

Faster and denser than chaining while the table is sparse, and much worse when it is not. Deletions need tombstones, which is real bookkeeping that chaining avoids entirely.

## Where it is used

Python's `dict` and `set`, Rust's `HashMap`, Google's dense_hash_map, and most performance-minded implementations.
