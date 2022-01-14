# Data structures

| Topic | |
|---|---|
| [doubly-linked-list](doubly-linked-list/) | two links, and what the second buys |
| [ring-buffer](ring-buffer/) | a queue with no allocation |
| [binary-search-tree](binary-search-tree/) | order as a structure, and the exam tasks |
| [hashtable](hashtable/) | two collision strategies, measured |
| [heap](heap/) | a tree with no links |

Each structure keeps one invariant, and every operation exists to preserve it.
The list keeps its links consistent, the ring buffer keeps its two positions
apart, the tree keeps its order condition, the hash table keeps its load
factor, and the heap keeps a parent at most its children.

The measurements say what the invariants are worth, and two of them are
uncomfortable. A search tree built from sorted input has depth 1023 instead of
10, so the structure that is supposed to be logarithmic is linear on the most
ordinary input there is. A hash table that does not grow reaches a longest
bucket of 42 with 500 keys in 16 buckets, so the constant-time lookup is
constant only while the table is mostly empty.

Every structure here is verified against its counterpart in the Java library
over hundreds of random operations, because the failures worth finding in this
kind of code are at the ends: the first element, the last one, the only one,
and the one that is not there.
