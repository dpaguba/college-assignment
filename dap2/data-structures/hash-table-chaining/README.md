# Hash table with separate chaining

A bucket per hash value, and a list in the bucket for collisions.

| Operation | Cost |
|---|---|
| Insert | O(1) average, O(n) worst |
| Search | O(1) average, O(n) worst |
| Delete | O(1) average, O(n) worst |
| Ordered traversal | not possible |

| | |
|---|---|
| Memory | O(n + buckets) |
| Ordered | no |

## The idea

The hash function turns a key into a bucket index, so a lookup goes straight to one
bucket instead of searching. Two keys landing in the same bucket is a collision,
and chaining handles it by keeping a list there.

Average O(1) rests on two conditions, and both can fail. The hash must spread keys
evenly: a bad one puts everything in one bucket and every operation becomes O(n).
That is not only a theoretical worry, it is an attack, hash flooding, and the reason
languages randomise their hash seed at startup. And the load factor must stay
bounded, which is what resizing enforces.

## How it works

Index by `hash(key) % capacity`, then walk the short list in that bucket. When the
count exceeds three quarters of the capacity, allocate double and rehash
everything.

That rehash makes one insert in n cost O(n), and amortised over the inserts that did
not resize it is still constant.

## The trade

Chaining tolerates a high load factor and deletes cleanly, but every collision is a pointer dereference into a separately allocated list. Open addressing keeps everything in one array and is faster to scan.

## Where it is used

Java's `HashMap`, most textbook implementations, and any table where deletions are frequent.
