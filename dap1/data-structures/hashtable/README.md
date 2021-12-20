# Hash table

Chapter eighteen, with both collision strategies.

| 500 keys | longest bucket |
|---|---:|
| 16 buckets, fixed | 42 |
| growing, load factor 0.49 | 4 |

The fixed table is the lecture's, and it degenerates exactly as the theory
says: forty-two keys deep in the worst bucket, so a lookup there costs
forty-two comparisons and the structure has become a list with extra steps.
Growing when the load factor passes 0.75 keeps the longest bucket at four.

The number that matters is the load factor, not the number of keys. That is
the whole content of the chapter: a hash table is fast while it is mostly
empty, and staying mostly empty means resizing, which means rehashing every
key, which is why the amortised cost is where the argument happens.

## Chaining against open addressing

Chaining puts colliding keys in a list at the bucket. Open addressing looks
for the next free slot. They differ on removal, and the difference is
instructive: a chain can drop an entry, while an open table must leave a mark,
because a later key may have been placed past this slot and a genuine gap
would end its search too early.

The mark is why open addressing degrades under heavy deletion: the marks are
occupied for searching and free for insertion, and a table full of them is
slow while looking empty. Both variants are checked against `HashMap` over
4000 random operations with deletions mixed in.

Everything here is measured rather than derived: `longestBucket` counts, and
`probesFor` counts what one lookup actually inspects. The two agree, which is
the check that the measurement means what it says.
